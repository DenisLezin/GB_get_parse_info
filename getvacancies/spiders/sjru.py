# -*- coding: utf-8 -*-
import scrapy
from getvacancies.items import GetvacanciesItem

vacancy_name = 'помощник бухгалтера'

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [f"http://superjob.ru/vacancy/search/?keywords={vacancy_name.replace(' ', '%20')}&geo%5Bc%5D%5B0%5D=1"]

    def parse(self, response):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancies = response.css('div.f-test-vacancy-item a[target="_blank"]::attr(href)').extract()

        for link in vacancies:
             yield response.follow(link, self.vacancy_parse)


    def vacancy_parse(self, response):
        pass
        request = vacancy_name
        vacancy = ' '.join(response.css('div.undefined h1 ::text').extract())
        location = ' '.join(response.css('div.undefined span._6-z9f ::text').extract())
        salary_min = response.css('div.undefined span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] ::text').extract()
        salary_max = None
        salary_currency = None
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