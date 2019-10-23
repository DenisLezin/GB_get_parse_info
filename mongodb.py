from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['test_mdb']

db.users