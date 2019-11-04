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

        if spider.name == 'sjru':
            if 'По договорённости' in item['salary_min']:
                item['salary_min'] = None
            elif 'от' in item['salary_min']:
                item['salary_currency'] = item['salary_min'][-1]
                item['salary_min'] = item['salary_min'][2]
            elif '—' in item['salary_min']:
                item['salary_max'] = item['salary_min'][4]
                item['salary_currency'] = item['salary_min'][-1]
                item['salary_min'] = item['salary_min'][0]
            else:
                item['salary_currency'] = item['salary_min'][-1]
                item['salary_min'] = item['salary_min'][0]


        collection = self.mongo_base[spider.name]
        collection.update_one(
            {"link": "item['link']"},
            {"$set": item},
            upsert=True)

        return item
