from lxml import html
import requests
from pprint import pprint
from numpy import datetime64


def get_mail_ru_news():
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

    mail_ru_requests = {'paths': '//div[@class="news-item o-media news-item_media news-item_main"]/a/@href |'
                                 '//div[@class="news-item__inner"]/a[not (@class)]/@href',
                        'news': '//h3[1]/text() |'
                                '//div[@class="news-item__inner"]/a[not (@class)]/text()',
                        'date': '//span[contains(@class, "js-ago")]/@datetime'}

    req = requests.get('https://mail.ru/', headers=header)

    ml_root = html.fromstring(req.text)

    ml_paths = ml_root.xpath(mail_ru_requests['paths'])

    ml_news = ml_root.xpath(mail_ru_requests['news'])

    items = []
    for i in range(len(ml_paths)):
        item = {'site': 'Mail.ru',
                'news': ml_news[i].replace('\xa0', ' '),
                'path': ml_paths[i],
                'date': datetime64(html.fromstring(requests.get(ml_paths[i], headers=header).text).xpath(
                    mail_ru_requests['date'])[0][:19])}
        items.append(item)
    return items



pprint(get_mail_ru_news())

