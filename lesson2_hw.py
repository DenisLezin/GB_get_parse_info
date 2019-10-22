from bs4 import BeautifulSoup as bs
import re
import requests
from pprint import pprint
import time

def get_salary_hh(vacancy_salary):
    vacancy_salary = vacancy_salary.getText().replace('\xa0', '')
    currency = re.search(r' \D+', vacancy_salary).group(0).replace('.', '').strip()
    if 'от' in vacancy_salary:
        vacancy_salary_min = re.findall(r'\d+', vacancy_salary)[0]
        vacancy_salary_max = None
    elif 'до' in vacancy_salary:
        vacancy_salary_min = None
        vacancy_salary_max = re.findall(r'\d+', vacancy_salary)[0]
    else:
        vacancy_salary_min = re.findall(r'\d+', vacancy_salary)[0]
        vacancy_salary_max = re.findall(r'\d+', vacancy_salary)[1]
    return [float(vacancy_salary_min) if vacancy_salary_min else None,
            float(vacancy_salary_max) if vacancy_salary_max else None,
            currency]

# Parse HH

main_link = 'https://hh.ru/search/vacancy'
vacancy = 'Python junior'
number_of_pages = 1

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
suffix = r'/?'+r'text=' + vacancy.replace(' ', '+')

# parsed = requests.get(main_link+suffix, headers=headers).text
with open('hh_content.txt', 'r', encoding='utf-8') as f:
   parsed = bs(f.read(), 'lxml')

result = []

for i in range(number_of_pages):
#    parsed = bs(requests.get(main_link+suffix, headers=headers).text, 'lxml')
    vacancy_block = parsed.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})

    for vac in vacancy_list:
        vacancy_data = {}

        vacancy_name = vac.find('a').getText()
        vacancy_city = re.search(r'^[\w-]+', vac.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()).group(0)
        vacancy_link = vac.find('a')['href']
        vacancy_salary = vac.find('div', {'class': 'vacancy-serp-item__salary'})
        if not vacancy_salary:
            vacancy_salary = [None, None, None]
        else:
            vacancy_salary = get_salary_hh(vacancy_salary)

        vacancy_data['vacancy'] = vacancy_name
        vacancy_data['city'] = vacancy_city
        vacancy_data['salary_min'] = vacancy_salary[0]
        vacancy_data['salary_max'] = vacancy_salary[1]
        vacancy_data['salary_currency'] = vacancy_salary[2]
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
#     print(i['salary'])
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
