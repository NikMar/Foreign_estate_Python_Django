# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, CommandError
from django.http import HttpResponse

import xml.etree.cElementTree as etree
import urllib2
import time

from foreign_estate.models import Object

# your custom command must reference the base management classes like this:
class Command(NoArgsCommand):
    # it's useful to describe what the function does:
    help = 'XML import to Database'

    def handle_noargs(self, **options):
		try:
			start_time = time.time()
			xmlDoc = urllib2.urlopen('http://tranio.ru/export-static/utf-8/digital_team.xml')

			xmlDocData = xmlDoc.read()
			xmlDocTree = etree.XML(xmlDocData)    
			
			ids = [str(x['id']).replace('L', '') for x in Object.objects.values('id')]	
			
			msg, msg2 = '', ''
			count_before = Object.objects.values('id').count()
			
			for object in xmlDocTree.iter('object'):
				kwargs, photos = {}, ''

				if object[0].text not in ids:
					for field in object:			
						if field.tag == 'address_splitted':
							for address in field:
								kwargs[address.tag] = address.text
						elif field.tag == 'photos':
							for url in field:
								photos += "{0} ".format(url.text)
							kwargs['photos'] = photos.split()				
						else:
							kwargs[field.tag] = field.text
					object = Object( **kwargs ).save()
					msg2 = 'База Обновлена'	
				else:
					msg = 'База Актуальна'

			count_after = Object.objects.values('id').count()	
			total_work_time = time.time() - start_time
			return 'Время работы: {0} cек.'.format(total_work_time)
		
		except urllib2.HTTPError, e:
			raise(e)

		