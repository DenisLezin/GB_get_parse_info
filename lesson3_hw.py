from lesson2_hw import get_vacancies
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacanies']
hh = db.hh

vacancy = 'Python junior'
number_of_pages = 5
min_salary = 60000

main_link = ['https://www.superjob.ru', 'https://hh.ru']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/77.0.3865.120 Safari/537.36'}

def fill_db(vacancy, number_of_pages, main_link, headers, test=True):
    hh.delete_many({})
    for link in main_link:
        hh.insert_many(get_vacancies(vacancy, number_of_pages, link, headers, test))

def get_vacancies_min_salary(salary):
    return hh.find({'salary_min':  {'$gte': salary}})


fill_db(vacancy, number_of_pages, main_link, headers, test=False)
objects = get_vacancies_min_salary(min_salary)
# objects = hh.find()

for obj in objects:
    pprint(obj)

print(hh.count_documents({}))
