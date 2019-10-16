import requests
import json
from pprint import pprint

user = 'user'
token = 'password'

def get_github_repos(user, token):
    repos_url = requests.get('https://api.github.com/user', auth=(user, token)).json()['repos_url']
    repos = requests.get(repos_url, auth=(user, token)).json()
    return [i['name'] for i in repos]


with open('github_repos.json', 'w') as f:
    f.write(json.dumps(get_github_repos(user, token)))

# pprint(get_github_repos(user, token))