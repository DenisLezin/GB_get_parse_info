# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class GetvacanciesPipeline(object):
    def __init__(self):
        client=MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.scrapy_vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.update_one(
            {"link": "item['link']"},
            {"$set": item},
            upsert=True)

        return item
