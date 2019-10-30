# -*- coding: utf-8 -*-
import scrapy


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['https://hh.ru/']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python']

    def parse(self, response):
        print(response)
        pass
