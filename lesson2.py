from bs4 import BeautifulSoup as bs
import requests

main_link = 'https://www.google.com/'
html = requests.get(main_link).text

pass