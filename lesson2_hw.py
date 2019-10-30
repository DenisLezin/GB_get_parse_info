from bs4 import BeautifulSoup as bs
import re
import requests
from pprint import pprint
import time
from random import randint


def request_to_file(file, link, headers, params):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(requests.get(link, headers=headers, params=params).text)


def get_vacancies(vacancy, number_of_pages, main_link, headers, test=True):

    request_params = get_params(main_link)

    suffix = eval(request_params['suffix'])

    if test:
        with open(request_params['test_file'], 'r', encoding='utf-8') as f:
            parsed = bs(f.read(), 'lxml')
        number_of_pages = 1

    result = []

    for i in range(number_of_pages):
        parsed = parsed if test else bs(requests.get(main_link+suffix, headers=headers).text, 'lxml')
        vacancy_block = eval(request_params['vacancy_block'])
        vacancy_list = eval(request_params['vacancy_list'])

        for vac in vacancy_list:
            vacancy_data = {}

            vacancy_name = eval(request_params['name'])

            vacancy_link = eval(request_params['link'])
            vacancy_salary = eval(request_params['salary'])
            vacancy_salary = get_salary(vacancy_salary)
            # print(vacancy_link)
            vacancy_city = eval(request_params['city'])

            vacancy_data['vacancy'] = vacancy_name
            vacancy_data['city'] = vacancy_city
            vacancy_data['salary_min'] = vacancy_salary[0]
            vacancy_data['salary_max'] = vacancy_salary[1]
            vacancy_data['salary_currency'] = vacancy_salary[2]
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = main_link

            result.append(vacancy_data)

        suffix = eval(request_params['next_page_suffix'])
        if not suffix:
            break
        else:
            suffix = suffix['href']
        time.sleep(randint(1, 3))
    return result


def get_salary(vacancy_salary):
    if not vacancy_salary or 'По договорённости' in vacancy_salary:
        return [None, None, None]

    vacancy_salary = vacancy_salary.getText().replace('\xa0', '')

    currency = re.search(r' \D+', vacancy_salary)

    if currency:
        currency = currency.group(0).replace('.', '').strip()
    else:
        currency = vacancy_salary[-1]

    if 'от' in vacancy_salary or '-' not in vacancy_salary:
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


def get_params(main_link):
    request_params_hh = {"suffix": "r'/search/vacancy/?'+r'text=' + vacancy.replace(' ', '+')",
                         "vacancy_block": "parsed.find('div', {'class': 'vacancy-serp'})",
                         "vacancy_list": "vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})",
                         "name": "vac.find('a').getText()",
                         "city": "re.search(r'^[\w-]+', vac.find('span', {'class': 'vacancy-serp-item__meta-info'})."
                                 "getText()).group(0)",
                         "link": "vac.find('a')['href']",
                         "salary": "vac.find('div', {'class': 'vacancy-serp-item__compensation'})",
                         "next_page_suffix": "parsed.find('a', {'data-qa': 'pager-next'})",
                         "test_file": "hh_content.txt"}

    request_params_superjob = {"suffix": "'/vacancy/search/?keywords={}'.format(vacancy.replace(' ', '%20'))",
                               "vacancy_block": "parsed.find('div', {'class': '_1ID8B'})",
                               "vacancy_list": "vacancy_block.find_all('div', {'class': "
                                               "'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})",
                               "name": "vac.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()",
                               "city": "re.search(r'• [\w-]+,?', vac.find('span', "
                                       "{'class': '_3mfro f-test-text-company-item-location _9fXTd _2JVkc _3e53o'})."
                                       "getText()).group(0)[2:].replace(',', '')",
                               "link": "main_link + vac.find('a')['href']",
                               "salary": "vac.find('span', {'class': "
                                         "'_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})",
                               "next_page_suffix": "parsed.find('a', {'class': "
                                                   "'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})",
                               "test_file": "superjob_content.txt"}

    if main_link == 'https://hh.ru':
        return request_params_hh
    elif main_link == 'https://www.superjob.ru':
        return request_params_superjob


# vacancy = 'Аналитик'
# number_of_pages = 2
#
# main_link_superjob = 'https://www.superjob.ru'
# main_link_hh = 'https://hh.ru'
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                          ' Chrome/77.0.3865.120 Safari/537.36'}
#
#
# res = get_vacancies(vacancy, number_of_pages, main_link_hh, headers, test=False)
#
# pprint(res)


# # request_to_file('superjob_content.txt', main_link+suffix, headers, None)
#
# def get_vacancies_hh(vacancy, number_of_pages, test=True):
#     # Parse HH
#
#     main_link = 'https://hh.ru/search/vacancy'
#
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
#     suffix = r'/?'+r'text=' + vacancy.replace(' ', '+')
#
#     if test:
#         with open('hh_content.txt', 'r', encoding='utf-8') as f:
#             parsed = bs(f.read(), 'lxml')
#         number_of_pages = 1
#     else:
#         parsed = requests.get(main_link+suffix, headers=headers).text
#
#     result = []
#
#     for i in range(number_of_pages):
#         parsed = parsed if test else bs(requests.get(main_link+suffix, headers=headers).text, 'lxml')
#         vacancy_block = parsed.find('div', {'class': 'vacancy-serp'})
#         vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})
#
#         for vac in vacancy_list:
#             vacancy_data = {}
#
#             vacancy_name = vac.find('a').getText()
#             vacancy_city = re.search(r'^[\w-]+', vac.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()).group(0)
#             vacancy_link = vac.find('a')['href']
#             vacancy_salary = vac.find('div', {'class': 'vacancy-serp-item__compensation'})
#             if not vacancy_salary:
#                 vacancy_salary = [None, None, None]
#             else:
#                 vacancy_salary = get_salary_hh(vacancy_salary, vacancy_name)
#
#             vacancy_data['vacancy'] = vacancy_name
#             vacancy_data['city'] = vacancy_city
#             vacancy_data['salary_min'] = vacancy_salary[0]
#             vacancy_data['salary_max'] = vacancy_salary[1]
#             vacancy_data['salary_currency'] = vacancy_salary[2]
#             vacancy_data['link'] = vacancy_link
#
#             result.append(vacancy_data)
#
#         suffix = parsed.find('a', {'data-qa': 'pager-next'})['href']
#         if not suffix:
#             break
#         else:
#             suffix = suffix[suffix.find('?'):]
#         time.sleep(randint(1, 3))
#     return result
