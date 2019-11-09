# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from lesson6_scrapy.avito.settings import IMAGES_STORE
import os

class AvitoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [os.path.join(IMAGES_STORE,
                              itm[1]["path"].split("/")[0], itm[1]["path"].split("/")[1]) for itm in results if itm[0]]
        return item

class DatabasePipeline(object):
    def __init__(self):
        client=MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.avito_parse

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
