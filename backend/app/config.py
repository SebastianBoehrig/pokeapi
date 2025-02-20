import yaml

def load_config():
    with open('config.yml', 'r') as f:
        return yaml.safe_load(f)

config = load_config()
POKEAPI_BASE_URL: str = config.get('pokeapi_base_url')
POKEAPI_POKEMON_URL: str = POKEAPI_BASE_URL + config.get('pokeapi_pokemon_path')
POKEAPI_SPECIES_URL: str = POKEAPI_BASE_URL + config.get('pokeapi_species_path')
POKEAPI_TYPE_URL: str = POKEAPI_BASE_URL + config.get('pokeapi_type_path')
HIGH_LIMIT: str = '?limit=10000'