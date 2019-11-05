# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lesson6_scrapy.avito.items import AvitoItem
from scrapy.loader import ItemLoader


class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()

        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        # photos = response.xpath('//div[contains(@class, "gallery-img-wrapper")]'
        #                         '//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        # temp = AvitoItem(photos=photos)
        # yield temp
        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title',
                       'h1.title-info-title span.item-info-title-text::text')
        yield loader.load_item()
