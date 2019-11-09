# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lesson6_scrapy.avito.items import AvitoItem
from scrapy.loader import ItemLoader


class AvitocarSpider(scrapy.Spider):
    name = 'avitocar'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']


    def parse(self, response: HtmlResponse):
        n = 1
        while True:
            next_page = response.css('a.js-pagination-next::attr(href)').extract_first()
            n += 1
            if n == 3:
                break
            yield response.follow(next_page, callback=self.parse)


        car_links = response.css('a.item-description-title-link::attr(href)').extract()

        for link in car_links:
            yield response.follow(link, self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//'
                         'div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title',
                       'h1.title-info-title span.title-info-title-text::text')
        loader.add_css('price',
                       'span.js-item-price::attr(content)')
        loader.add_css('price', 'span.price-value-prices-list-item-currency_sign::attr(content)')
        loader.add_value('link',
                         response.url)
        loader.add_xpath('params', '//li[@class="item-params-list-item"]//text()')

        yield loader.load_item()





