import requests
from pprint import pprint

base_url = 'https://pokeapi.co/api/v2/'

pokemon_url = f'{base_url}/pokemon/'

# response = requests.get(f'{pokemon_url}/ditto')
# print(response.status_code)
# pprint(response.json())

def get_all_pokemon():
    response = requests.get(f'{pokemon_url}?limit=10')
    pprint(response.json())
    pokemon_obj=response.json()['results']
    return [pokemon['name'] for pokemon in pokemon_obj]

pprint(get_all_pokemon())