# -*- coding: utf-8 -*-

# Фильтруем по полю purpose
def filterByPurpose(qs, params):
    purpose = params['purpose']
    if purpose == 's':
        qs = qs.filter(purpose__in = ['s', 'sr'])
    elif purpose == 'r':
    	qs = qs.filter(purpose__in = ['r', 'sr'])
    return qs


# Фильтруем по полю country
def filterByCountry(qs, params):
	countries = params['countries']
	if countries:
		qs = qs.filter(country__in = countries)
	return qs


# Фильтруем в списке значений (страны)
def filterByFieldWithEnum(qs, params, param_name, field_name):
	filterEnum = params[param_name]
	if filterEnum:
		qs = qs.filter( **{"{0}__in".format(field_name): filterEnum} )
	return qs


# Фильтурем в промежутке значений (площадь, цена и тд.)
def filterByFieldWithRange(qs, params, param_name, field_name):
    filterRange = params[param_name]
    if filterRange:
        qs = qs.filter( **{"{0}__range".format(field_name): (filterRange[0], filterRange[1])} )  
    return qs


# Фильтруем по количеству комнат
def filterByRoomAmount(qs, params):
	room_amount = params['room_amount']
	if room_amount:
		if 5 in room_amount:
			qs = qs.filter(rooms_living__in = room_amount, rooms_living__gt = 5)
		else:
			qs = qs.filter(rooms_living__in = room_amount)
	return qs  