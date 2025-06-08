import asyncio
from pprint import pprint

import httpx
from fastapi import HTTPException

from app.logic.get_pokemon_primitive import get_pokemon_primitive
from app.logic.helpers import extract_img_from_raw_pokemon_sprites
from app.pokeapi_requests import get_evolution_chain, get_pokemon, get_pokemon_species
from app.types import (
    EvolutionChain,
    EvolutionTaskTree,
    EvolutionTree,
    PokemonDetail,
    PokemonImg,
    PokemonPrimitive,
    PokemonSpecies,
    RawPokemon,
    RawPokemonType,
)


async def get_pokemon_detail(pokemon_name: str, client: httpx.AsyncClient) -> PokemonDetail:
    pokemon: RawPokemon = await get_pokemon(pokemon_name, client)

    types: list[str | None] = _extract_types_from_raw_pokemon_types(pokemon.get('types', []))
    img: PokemonImg = extract_img_from_raw_pokemon_sprites(pokemon.get('sprites', {}))
    weight, height = _extract_data_points_from_raw_pokemon(pokemon)

    species_name: str | None = pokemon.get('species', {}).get('name')
    if not species_name:
        raise HTTPException(status_code=404, detail=f'species of {pokemon_name} not found, (get_pokemon_detail)')
    species: PokemonSpecies = await get_pokemon_species(species_name, client)

    # varieties
    raw_varietie_task_list: list[asyncio.Task[RawPokemon]] = []
    varietie_list: list[PokemonPrimitive] = []
    async with asyncio.TaskGroup() as tg:
        for varietie in species.get('varieties', {}):
            if not varietie.get('pokemon'):
                continue
            varietie_name: str | None = varietie.get('pokemon', {}).get('name')
            if not varietie_name or varietie_name == pokemon.get('name'):
                continue

            task: asyncio.Task[RawPokemon] = tg.create_task(get_pokemon(varietie_name, client))
            raw_varietie_task_list.append(task)

    for done_task in raw_varietie_task_list:
        raw_pokemon: RawPokemon = done_task.result()
        pokemonImg: PokemonImg = extract_img_from_raw_pokemon_sprites(raw_pokemon.get('sprites', {}))
        varietie_list.append({'name': raw_pokemon.get('name', ''), 'img': pokemonImg.get('default')})

    # evolution tree
    evolution_url: str | None = species.get('evolution_chain', {}).get('url')
    evolution_tree: EvolutionTree | None = None
    if evolution_url:
        chain: EvolutionChain = await get_evolution_chain(evolution_url, client)
        evolution_tree = await _extract_evolution_tree(chain, client)

    # Build return object
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


def _extract_types_from_raw_pokemon_types(raw_pokemon_types: list[RawPokemonType]) -> list[str | None]:
    return [type.get('type', {}).get('name') for type in raw_pokemon_types]


def _extract_data_points_from_raw_pokemon(pokemon: RawPokemon) -> tuple[float | None, int | None]:
    weight = pokemon.get('weight', None)
    height = pokemon.get('height', None)
    if weight:
        weight /= 10  # pokeapi only has cg and rounds up
    if height:
        height *= 10  # pokeapi only has dm and rounds up
    return weight, height


async def _extract_evolution_tree(chain_root: EvolutionChain, client: httpx.AsyncClient) -> EvolutionTree | None:
    if not chain_root.get('evolves_to'):
        return None
    try:
        tasktree: EvolutionTaskTree
        async with asyncio.TaskGroup() as tg:
            tasktree = await _resolve_tree_recursive(chain_root, client, tg)
        return _extract_evolution_tree_from_task_tree_recursive(tasktree)
    except Exception as e:
        pprint('error in the recursive evolution tree resolution!')
        pprint(e)
        return None


async def _resolve_tree_recursive(
    chain: EvolutionChain, client: httpx.AsyncClient, tg: asyncio.TaskGroup
) -> EvolutionTaskTree:
    name: str = chain.get('species').get('name')
    task: asyncio.Task[PokemonPrimitive] = tg.create_task(get_pokemon_primitive(name, client))
    if not chain.get('evolves_to'):
        return {'task': task, 'task_tree': None}
    else:
        evolutions: list[EvolutionTaskTree] = [
            await _resolve_tree_recursive(entry, client, tg) for entry in chain.get('evolves_to')
        ]
        return {'task': task, 'task_tree': evolutions}


def _extract_evolution_tree_from_task_tree_recursive(task_tree: EvolutionTaskTree) -> EvolutionTree:
    evolution: list[EvolutionTree] | None = None
    inner_tree_list = task_tree.get('task_tree')
    if inner_tree_list:
        evolution = [
            _extract_evolution_tree_from_task_tree_recursive(inner_task_tree) for inner_task_tree in inner_tree_list
        ]
    return {
        'pokemonPrimitive': task_tree.get('task').result(),
        'evolvesTo': evolution,
    }
