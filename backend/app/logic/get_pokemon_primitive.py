import httpx
from fastapi import HTTPException

from app.logic.helpers import extract_img_from_raw_pokemon_sprites
from app.pokeapi_requests import get_pokemon, get_pokemon_species
from app.types import PokemonImg, PokemonListEntry, PokemonPrimitive, PokemonSpecies, RawPokemon, Varieties


async def get_pokemon_primitive(species_name: str, client: httpx.AsyncClient) -> PokemonPrimitive:
    species: PokemonSpecies = await get_pokemon_species(species_name, client)

    varieties_list: list[Varieties] | None = species.get('varieties')
    if not varieties_list:
        raise HTTPException(status_code=404, detail=f'variety of {species_name} not found, (get_pokemon_primitive)')

    default_varietie_name: str | None = _extract_default_varietie_name(varieties_list)
    if default_varietie_name is None:
        raise HTTPException(
            status_code=404, detail=f'default varietie of {species_name} not found, (get_pokemon_primitive)'
        )

    default_pokemon: RawPokemon = await get_pokemon(default_varietie_name, client)

    pokemonImg: PokemonImg = extract_img_from_raw_pokemon_sprites(default_pokemon.get('sprites', {}))
    return {'name': species.get('name', species_name), 'img': pokemonImg.get('default')}

def _extract_default_varietie_name(varietie_list: list[Varieties]) -> str | None:
    for varietie in varietie_list:
        if varietie.get('is_default'):
            entry: PokemonListEntry = varietie.get('pokemon', {})
            return entry.get('name')
    return None