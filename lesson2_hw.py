from bs4 import BeautifulSoup as bs
import re
import requests
from pprint import pprint
import time

def get_compensation_hh(vacancy_compensation):
    vacancy_compensation = vacancy_compensation.getText().replace('\xa0', '')
    currency = re.findall(r' \D+', vacancy_compensation)[0]
    if 'от' in vacancy_compensation:
        vacancy_compensation_min = re.findall(r'\d+', vacancy_compensation)[0]
        vacancy_compensation_max = 'Undefined'
    elif 'до' in vacancy_compensation:
        vacancy_compensation_min = 'Undefined'
        vacancy_compensation_max = re.findall(r'\d+', vacancy_compensation)[0]
    else:
        vacancy_compensation_min = re.findall(r'\d+', vacancy_compensation)[0]
        vacancy_compensation_max = re.findall(r'\d+', vacancy_compensation)[1]
    return [vacancy_compensation_min, vacancy_compensation_max, currency]

# Parse HH

main_link = 'https://hh.ru/search/vacancy'
vacancy = 'Python junior'
number_of_pages = 2

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
suffix = r'/?'+r'text=' + vacancy.replace(' ', '+')

# parsed = requests.get(main_link+suffix, headers=headers).text
# with open('hh_content.txt', 'r', encoding='utf-8') as f:
#    parsed = bs(f.read(), 'lxml')

result = []

for i in range(number_of_pages):
    parsed = bs(requests.get(main_link+suffix, headers=headers).text, 'lxml')
    vacancy_block = parsed.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})

    for vac in vacancy_list:
        vacancy_data = {}

        vacancy_name = vac.find('a').getText()
        vacancy_link = vac.find('a')['href']
        vacancy_compensation = vac.find('div', {'class': 'vacancy-serp-item__compensation'})
        if not vacancy_compensation:
            vacancy_compensation = ['Undefined', 'Undefined', '']
        else:
            vacancy_compensation = get_compensation_hh(vacancy_compensation)

        vacancy_data['vacancy'] = vacancy_name
        vacancy_data['compensation_min'] = str(vacancy_compensation[0]) + vacancy_compensation[2]
        vacancy_data['compensation_max'] = str(vacancy_compensation[1]) + vacancy_compensation[2]
        vacancy_data['link'] = vacancy_link

        result.append(vacancy_data)

    suffix = parsed.find('a', {'data-qa': 'pager-next'})['href']
    if not suffix:
        break
    else:
        suffix = suffix[suffix.find('?'):]
    time.sleep(1)


pprint(result)



# for i in result:
#     print(i['compensation'])
#
#
#
#
#
#
#
#
#
#
# with open('hh_content.txt', 'w', encoding='utf-8') as f:
#     f.write(requests.get(main_link, headers=headers, params=params).text)
