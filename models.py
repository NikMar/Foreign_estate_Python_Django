# -*- coding: utf-8 -*-
from django.db import models

class Object(models.Model):

	url = models.CharField(max_length=400, null=True, blank=True)
	date = models.CharField(max_length=100, null=True, blank=True)
	
	# e - евро, r - рубли, u - доллары, p - фунты
	currency = models.CharField(max_length=1, null=True, blank=True)
	price_sell = models.BigIntegerField(null=True, blank=True)
	price_rent_monthly = models.IntegerField(null=True, blank=True)
	price_rent_weekly = models.IntegerField(null=True, blank=True)
	
	address = models.CharField(max_length=500, null=True, blank=True)
	country = models.CharField(max_length=200, null=True, blank=True)
	region = models.CharField(max_length=200, null=True, blank=True)
	locality = models.CharField(max_length=200, null=True, blank=True)

	lat = models.CharField(max_length=100, null=True, blank=True)
	lng = models.CharField(max_length=100, null=True, blank=True)

	# s - продажа, r - аренда, sr - продажа и аренда
	purpose = models.CharField(max_length=2, null=True, blank=True)

	# object_type
	# a - Коттедж
	# b - Вилла
	# c - Дом в городе
	# d - Квартира
	# e - Таунхаус
	# f - Замок
	# g - Поместье
	# h - Особняк
	# s - Шале
	# i - Коммерческий центр
	# l - Развлекательный комплекс
	# j - Офис
	# k - Отель
	# m - Спорткомплекс
	# q - Доходный дом
	# r - Торговая недвижимость
	# t - Ресторан
	# u - АЗС
	# v - Склад
	# w - Инвестиционный проект
	# o - Земельный участок
	# p - Ферма, сельхозугодья
	# n - Виноградник
	object_type = models.CharField(max_length=1, null=True, blank=True)
	
	area_object = models.IntegerField(null=True, blank=True)
	area_land = models.IntegerField(null=True, blank=True)
	area_living = models.IntegerField(null=True, blank=True)
	construction_year = models.IntegerField(null=True, blank=True)
	rooms_living = models.IntegerField(null=True, blank=True)
	rooms_combined = models.IntegerField(null=True, blank=True)
	floors = models.IntegerField(null=True, blank=True)
	floor = models.IntegerField(null=True, blank=True)
	bathrooms = models.IntegerField(null=True, blank=True)
	rooms_sauna = models.IntegerField(null=True, blank=True)

    # для pool, garden, parking: p - частная, s - общая
	pool = models.CharField(max_length=1, null=True, blank=True)
	garden = models.CharField(max_length=1, null=True, blank=True)
	parking = models.CharField(max_length=1, null=True, blank=True) 
    
	price_sell_e = models.BigIntegerField(null=True, blank=True)
	price_sell_u = models.BigIntegerField(null=True, blank=True)
	price_sell_r = models.BigIntegerField(null=True, blank=True)

	balcony = models.IntegerField(null=True, blank=True)
	window_view = models.IntegerField(null=True, blank=True)
	terrace = models.IntegerField(null=True, blank=True)
	internet = models.IntegerField(null=True, blank=True)
	wc = models.IntegerField(null=True, blank=True)
	tv = models.IntegerField(null=True, blank=True)
	fitness = models.IntegerField(null=True, blank=True)
	furnished = models.IntegerField(null=True, blank=True)
	first_line = models.IntegerField(null=True, blank=True)
	garage = models.IntegerField(null=True, blank=True)
	garage_cars = models.IntegerField(null=True, blank=True)
	personal_beach = models.IntegerField(null=True, blank=True)
	private_gym = models.IntegerField(null=True, blank=True)
	supermarket = models.IntegerField(null=True, blank=True)
	private_tennis_court = models.IntegerField(null=True, blank=True)
	rooms_terrace = models.IntegerField(null=True, blank=True)
	rooms_balcony = models.IntegerField(null=True, blank=True)
	private_territory = models.IntegerField(null=True, blank=True)

	# a - Поле для гольфа, b - Гольф-клуб, c - Гольф-курорт и их комбинации: ab, ac, bc, abc
	golf = models.CharField(max_length=3, null=True, blank=True)
	golf_field = models.CharField(max_length=3, null=True, blank=True)          

	distance_parking = models.IntegerField(null=True, blank=True)  
	distance_supermarket = models.IntegerField(null=True, blank=True)
	distance_sea = models.IntegerField(null=True, blank=True)
	distance_mountains = models.IntegerField(null=True, blank=True)

	description_short = models.CharField(max_length=500, null=True, blank=True)
	description_full = models.TextField(null=True, blank=True)

	photos = models.TextField(null=True, blank=True)