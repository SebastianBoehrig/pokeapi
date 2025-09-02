import os

import yaml

config_path: str = os.path.join(os.path.dirname(__file__), '..', 'config.yml')


def load_config() -> dict[str, str]:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


config: dict[str, str] = load_config()
POKEAPI_BASE_URL: str = config.get('pokeapi_base_url', '')
POKEAPI_POKEMON_URL: str = POKEAPI_BASE_URL + '/' + config.get('pokeapi_pokemon_path', '')
POKEAPI_SPECIES_URL: str = POKEAPI_BASE_URL + '/' + config.get('pokeapi_species_path', '')
POKEAPI_TYPE_URL: str = POKEAPI_BASE_URL + '/' + config.get('pokeapi_type_path', '')
HIGH_LIMIT: str = '?limit=10000'
