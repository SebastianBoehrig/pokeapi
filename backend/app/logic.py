from __future__ import annotations

from pprint import pprint
from typing import Dict, Union

from fastapi import HTTPException
from glom import Coalesce, glom
from typing_extensions import TypedDict

from app.pokeapi_requests import (
    EvolutionChain,
    PokemonListEntry,
    PokemonSpecies,
    RawPokemon,
    RawPokemonType,
    RawType,
    Varieties,
    get_evolution_chain,
    get_pokemon,
    get_pokemon_species,
    get_type,
)


class PokemonPrimitive(TypedDict):
    name: str
    img: str | None


class PokemonImg(TypedDict):
    default: str | None
    shiny: str | None


class EvolutionTree(TypedDict):
    pokemonPrimitive: PokemonPrimitive
    evolvesTo: list['EvolutionTree'] | None


class PokemonDetail(TypedDict):
    name: str
    weight: float | None
    height: int | None
    types: list[str | None]
    img: PokemonImg
    varietieTypes: list[PokemonPrimitive]
    cosmeticTypes: list[PokemonPrimitive] | None
    evolutionTree: EvolutionTree | None


def get_pokemon_primitive(species_name: str) -> PokemonPrimitive:
    species: PokemonSpecies = get_pokemon_species(species_name)

    varieties_list: list[Varieties] | None = species.get('varieties')
    if not varieties_list:
        raise HTTPException(status_code=404, detail=f'variety of {species_name} not found, (get_pokemon_primitive)')

    default_varietie_name: str | None = _extract_default_varietie_name(varieties_list)
    if default_varietie_name is None:
        raise HTTPException(
            status_code=404, detail=f'default varietie of {species_name} not found, (get_pokemon_primitive)'
        )

    default_pokemon: RawPokemon = get_pokemon(default_varietie_name)

    pokemonImg: PokemonImg = _extract_img_from_raw_pokemon_sprites(default_pokemon.get('sprites', {}))
    return {'name': species.get('name'), 'img': pokemonImg.get('default')}


def get_pokemon_detail(pokemon_name: str) -> PokemonDetail:
    pokemon: RawPokemon = get_pokemon(pokemon_name)

    types: list[str | None] = _extract_types_from_raw_pokemon_types(pokemon.get('types', []))
    img: PokemonImg = _extract_img_from_raw_pokemon_sprites(pokemon.get('sprites', {}))
    weight, height = _extract_data_points_from_raw_pokemon(pokemon)

    species_name: str | None = pokemon.get('species', {}).get('name')
    if not species_name:
        raise HTTPException(status_code=404, detail=f'species of {pokemon_name} not found, (get_pokemon_detail)')
    species: PokemonSpecies = get_pokemon_species(species_name)

    # varieties
    varietie_list: list[PokemonPrimitive] = []
    for varietie in species.get('varieties', {}):
        if not varietie.get('pokemon'):
            continue
        varietie_name: str | None = varietie.get('pokemon', {}).get('name')
        if varietie_name and varietie_name != pokemon.get('name'):
            raw_pokemon: RawPokemon = get_pokemon(varietie_name)

            pokemonImg: PokemonImg = _extract_img_from_raw_pokemon_sprites(raw_pokemon.get('sprites', {}))
            varietie_list.append({'name': varietie_name, 'img': pokemonImg.get('default')})

    # evolution Tree
    evolution_url: str | None = species.get('evolution_chain', {}).get('url')
    evolution_tree: EvolutionTree | None = None
    if evolution_url:
        chain: EvolutionChain = get_evolution_chain(evolution_url)
        evolution_tree = _extract_evolution_tree(chain)
    # Build return Object

    return {
        'name': pokemon.get('name', pokemon_name),
        'weight': weight,
        'height': height,
        'types': types,
        'img': img,
        'varietieTypes': varietie_list,
        'cosmeticTypes': None,
        'evolutionTree': evolution_tree,
    }


def get_pokemon_primitive_of_type(type_name: str) -> list[PokemonPrimitive]:
    type: RawType = get_type(type_name)

    pokemon_name_list: list[str] = []
    for raw_type_pokemon in type.get('pokemon', {}):
        pokemon_name: str | None = raw_type_pokemon.get('pokemon', {}).get('name')
        if pokemon_name:
            pokemon_name_list.append(pokemon_name)

    result: list[PokemonPrimitive] = []
    for name in pokemon_name_list:
        pokemon: RawPokemon = get_pokemon(name)

        pokemonImg: PokemonImg = _extract_img_from_raw_pokemon_sprites(pokemon.get('sprites', {}))
        result.append({'name': name, 'img': pokemonImg.get('default')})
    return result


def _extract_default_varietie_name(varietie_list: list[Varieties]) -> str | None:
    for varietie in varietie_list:
        if varietie.get('is_default'):
            entry: PokemonListEntry = varietie.get('pokemon', {})
            return entry.get('name')
    return None


def _extract_types_from_raw_pokemon_types(raw_pokemon_types: list[RawPokemonType]) -> list[str | None]:
    return [type.get('type', {}).get('name') for type in raw_pokemon_types]


def _extract_img_from_raw_pokemon_sprites(
    raw_pokemon_sprites: Dict[str, Union[str, Dict[str, Dict[str, str]]]],
) -> PokemonImg:
    return glom(
        raw_pokemon_sprites,
        {
            'default': Coalesce('other.official-artwork.front_default', 'front_default', default=None, skip=None),
            'shiny': Coalesce('other.official-artwork.front_shiny', 'front_shiny', default=None, skip=None),
        },
    )


def _extract_data_points_from_raw_pokemon(pokemon: RawPokemon) -> tuple[float | None, int | None]:
    weight = pokemon.get('weight', None)
    height = pokemon.get('height', None)
    if weight:
        weight /= 10  # pokeapi only has dm and rounds up
    if height:
        height *= 10  # pokeapi only has dm and rounds up
    return weight, height


def _extract_evolution_tree(chain_root: EvolutionChain) -> EvolutionTree | None:
    if not chain_root.get('evolves_to'):
        return None
    try:
        return _resolve_tree_recursive(chain_root)
    except Exception as e:
        pprint(e)
        return None


def _resolve_tree_recursive(chain: EvolutionChain) -> EvolutionTree:
    name: str = chain.get('species').get('name')
    primitive: PokemonPrimitive = get_pokemon_primitive(name)

    if not chain.get('evolves_to'):
        return {'pokemonPrimitive': primitive, 'evolvesTo': None}
    else:
        evolutions: list[EvolutionTree] = [_resolve_tree_recursive(entry) for entry in chain.get('evolves_to')]
        return {'pokemonPrimitive': primitive, 'evolvesTo': evolutions}
