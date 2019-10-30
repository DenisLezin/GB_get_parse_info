# -*- coding: utf-8 -*-
import scrapy


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['https://www.superjob.ru/']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):
        print(response)
        pass
