# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Object

from jqestate import render_to_json
from jqestate.items_for_page import itemsForPageByParams

import rubru.jq_json, json
import foreign_filter

# Используя этот декоратор над вью мы добиваемся следующего:
# 1. Результирующий вью возвращает рендер HTML шаблона render(request, templateName, locals())
# 2. Декорируемый вью должен вернуть переменные для подстановки в шаблон
# 3. Если в запросе есть параметр api, то в качестве шаблона используется специальный темплейт.
# автоматически генерит справку по серверному АПИ для верстальщиков
def render_with_api(templateName):
    def render_with_api_decor(f):
        def render_with_api_wrapper(request, *args, **kwargs):
            realTemplateName = templateName
            contextList = f(request, *args, **kwargs)

            # Если указан параметр api в запросе то генерим справку для верстальщиков по серверному АПИ
            if 'api' in request.GET:
                realTemplateName = 'api_page.html'
                contextList['jq_api_vars'] = []
                contextList['jq_api_template_name'] = templateName

                for k, v in contextList.iteritems():

                    # Саму себя и переменную request что есть во view включать тут в справку не нужно.
                    # request не рендерится в json к тому же.
                    if k not in ['jq_api_vars', 'jq_api_template_name', 'request']:
                        contextList['jq_api_vars'].append({
                            'name': k,
                            'value': v
                        })
            return render(request, realTemplateName, contextList)
        return render_with_api_wrapper

    return render_with_api_decor

# Используя этот декоратор над вью мы добиваемся следующего:
# 1. Добавляем справку по api для ajax
# 2. Ожидаем как return из декорируемый функции Питон-Объект, который сериализуется в JSON
# Декоратору в аргументх можно писать GET = dict, POST = dict, тогда
# dict будет использоваться в качестве примера для GET и POST запроса.
def render_with_ajax_api(**kwargs):
    def render_with_api_decor(f):
        def render_with_api_wrapper(request, *args2, **kwargs2):

            # Если указан параметр api в запросе то генерим справку для верстальщиков по серверному АПИ
            if 'api' in request.GET:
                import json
                contextVars = {}
                if 'POST' in kwargs:
                    contextVars['jq_api_example_post_request_json'] = kwargs['POST']
                if 'GET' in kwargs:
                    def urlize(dict):
                        r = []
                        for k, v in dict.items():
                            r.append(u'{0}={1}'.format(k, v))
                        return '&'.join(r)
                    contextVars['jq_api_example_get_request_url'] = kwargs['GET']
                return render(request, 'api_page_ajax.html', contextVars)

            res = f(request, *args2, **kwargs2)
            import jqbase2.jq_file_upload
            return jqbase2.jq_file_upload.JsonResponse(request, res)

        return render_with_api_wrapper

    return render_with_api_decor



# Запрос Аякс список Зарубежной недвижимости
foreign_objects_ajax_example = """{
    // Тип спроса по которому получить информацию: купить 's', снять 'r', купить\снять 'sr'
    "purpose": "s",
    // Количество объектов на странице (задает размер выдачи и то какие объекты попадут на страницу page_number)
    "objects_per_page": 20,
    // Текущая страница, объекты с которой нужно показать
    "page_number": 1,
    // Фильтрация по страницам
    "countries": [],
    // Фильтрация по типу аппартаментов
    "object_types": [],
    // Фильтрация по площади
    "area_living": [],
    // Фильтрация по цене
    "price_sell_u": [],
    // Филтруем по этажам
    "floor": [],
    // Фильтруем по этажей в доме
    "floors": []  
}"""

@csrf_exempt
@render_with_ajax_api(POST = foreign_objects_ajax_example)
def foreign_objects_ajax(request):

   # Получаем параметры запроса
    import json
    params = json.loads(request.POST['query']) 

    # Получаем полный список объектов
    objects = Object.objects.all()
    
    # Фильтрация   
    objects = foreign_filter.filterByPurpose(objects, params)
    #objects = foreign_filter.filterByRoomAmount(objects, params)
    
    objects = foreign_filter.filterByFieldWithEnum(objects, params, 'countries', 'country')
    objects = foreign_filter.filterByFieldWithEnum(objects, params, 'object_types', 'object_type')
    #objects = foreign_filter.filterByFieldWithEnum(objects, params, 'ids', 'id')
    
    objects = foreign_filter.filterByFieldWithRange(objects, params, 'area_living', 'area_living')
    objects = foreign_filter.filterByFieldWithRange(objects, params, 'price_sell_u', 'price_sell_u')
    objects = foreign_filter.filterByFieldWithRange(objects, params, 'floor', 'floor')
    objects = foreign_filter.filterByFieldWithRange(objects, params, 'floors', 'floors')    
    
    # Количество объектов
    total_count = objects.count()

  	# Разбивка по страницам. Важно - на последнем этапе.   
    objects = itemsForPageByParams(objects, params)
   
    # Итог - питон-объект - для сериализации в JSON.
    return {
        'objects': json.dumps(objects, cls=render_to_json.ObjectsJSONEncoder),
     	'total_count': total_count     	
    }


@render_with_api('international_realty/buy.html')
def buy(request):

    countries = json.dumps(Object.objects.values('country').distinct(), cls=render_to_json.ObjectsJSONEncoder)
    ids = json.dumps(Object.objects.values('id'), cls=render_to_json.ObjectsJSONEncoder)
    return locals()


@render_with_api('international_realty/rent.html')
def rent(request):
    
    countries = json.dumps(Object.objects.values('country').distinct(), cls=render_to_json.ObjectsJSONEncoder)
    ids = json.dumps(Object.objects.values('id'), cls=render_to_json.ObjectsJSONEncoder)
    return locals()


# Карточка объекта Зарубежной недвижимости
@render_with_api('international_realty/object.html')
def object(request, requestType, objectId):

    object = Object.objects.get(id = objectId)
    
    # Цены в доллрах и рублях
    object.price_sell_u = "{:,} $".format(object.price_sell_u).replace(',', ' ')
    object.price_sell_r = "{:,} руб".format(object.price_sell_r).replace(',', ' ')   

    # Площадь дома
    object.area_object = "{0} кв.м.".format(object.area_object)

    # Описание, вырезаем теги
    import re
    object.description_full = re.sub('<[^>]*>', '',  object.description_full)
    
    # Особенности
    def boolToPresentOrNoStr(val):
    	return u"Есть" if val else u"Нет"
    
    object.balcony = boolToPresentOrNoStr(object.balcony)
    object.terrace = boolToPresentOrNoStr(object.terrace)
    object.internet = boolToPresentOrNoStr(object.internet)
    
    import ast    
    object.photos = ast.literal_eval(object.photos)
    return locals()