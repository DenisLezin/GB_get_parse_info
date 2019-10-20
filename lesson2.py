from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


main_link = 'https://www.kinopoisk.ru'
suffix = '/afisha/new/city/1/'

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

parsed = requests.get(main_link+suffix, headers=headers).text
# with open('site_content.txt', 'r', encoding='utf-8') as f:
#     parsed = bs(f.read(), 'lxml')

films_block = parsed.find('div', {'class': 'filmsListNew'})
films_list = films_block.findChildren(recursive=False)

films = []

for film in films_list:
    film_data = {}
    film_info = film.find('div', {'class': 'name'}).findChild()

    film_name = film_info.getText()
    film_link = main_link+film_info['href']
    genre = film.find_all('div', {'class': 'gray'})[1].getText().replace(' ', '')[9:]
    rating = film.find('span', {'class': ['rating_ball_green', 'rating_ball_red', 'rating_ball_grey']})
    rating = 0 if not rating else rating.getText()
    # print('-' * 200, film_name, film_link, genre, rating, sep='\n')
    film_data['name'] = film_name
    film_data['genre'] = genre
    film_data['rating'] = rating
    film_data['link'] = film_link
    films.append(film_data)

pprint(films)