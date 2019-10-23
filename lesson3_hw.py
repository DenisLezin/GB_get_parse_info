from lesson2_hw import get_vacancies_hh
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacanies']
hh = db.hh

vacancy = 'Python junior'
number_of_pages = 5
min_salary = 60000

def fill_db(vacancy, number_of_pages, test=True):
    hh.delete_many({})
    hh.insert_many(get_vacancies_hh(vacancy, number_of_pages, test))

def get_vacancies_min_salary(salary):
    return hh.find({'salary_min':  {'$gte': salary}})


fill_db(vacancy, number_of_pages, test=False)
objects = get_vacancies_min_salary(min_salary)
# objects = hh.find()

for obj in objects:
    pprint(obj)

print(hh.count_documents({}))
