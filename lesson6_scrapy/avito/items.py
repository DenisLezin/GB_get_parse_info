# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photos(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def make_params(params):
    if params:
        return {i[0]: i[1] for i in zip(params[1::3], params[2::3])}


def convert_price(price):
    return [float(price[0]), price[1]]


class AvitoItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photos))
    price = scrapy.Field(input_processor=TakeFirst(), output_processor=convert_price)
    link = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(output_processor=make_params)

