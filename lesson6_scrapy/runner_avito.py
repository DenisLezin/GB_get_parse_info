from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson6_scrapy.avito import settings
from lesson6_scrapy.avito.spiders.avitoru import AvitoruSpider
from lesson6_scrapy.avito.spiders.avitocar import AvitocarSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
#    process.crawl(AvitoruSpider)
    process.crawl(AvitocarSpider)
    process.start()
