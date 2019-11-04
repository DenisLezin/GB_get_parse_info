# -*- coding: utf-8 -*-
import scrapy
from getvacancies.items import GetvacanciesItem

vacancy_name = 'data scientist'

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [f"https://hh.ru/search/vacancy?text={vacancy_name.replace(' ', '+')}"]

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancies = response.css('a[data-qa="vacancy-serp__vacancy-title"]::attr(href)').extract()

        for link in vacancies:
             yield response.follow(link, self.vacancy_parse)


    def vacancy_parse(self, response):
        request = vacancy_name
        vacancy = ' '.join(response.css('div.vacancy-title h1.header ::text').extract())
        location = response.css('div.vacancy-company p:nth-child(2) ::text').extract_first()
        salary_min = response.css('div.vacancy-title meta[itemprop="minValue"] ::attr(content)').extract_first()
        salary_max = response.css('div.vacancy-title meta[itemprop="maxValue"] ::attr(content)').extract_first()
        salary_currency = response.css('div.vacancy-title meta[itemprop="currency"] ::attr(content)').extract_first()
        link = response.url
        yield GetvacanciesItem(
            request=request,
            vacancy=vacancy,
            location=location,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_currency=salary_currency,
            link=link
        )

