import requests
from pprint import pprint

user = 'DenisLezin'
token = 'b15165f06e8c2578be0986e9a5f36b972a025bb0'

def get_github_repos(user, token):
    repos_url = requests.get('https://api.github.com/user', auth=(user, token)).json()['repos_url']
    repos = requests.get(repos_url, auth=(user, token)).json()
    return [i['name'] for i in repos]


pprint(get_github_repos(user, token))