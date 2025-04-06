from __future__ import annotations

import asyncio
from typing import Dict, Union

from typing_extensions import TypedDict


class TypesType(TypedDict):
    name: str
    img: str


class PokemonListEntry(TypedDict):
    name: str
    url: str


class RawPokemonType(TypedDict):
    slot: int
    type: PokemonListEntry


class EvolutionChain(TypedDict):
    evolves_to: list['EvolutionChain']
    species: PokemonListEntry


class Varieties(TypedDict):
    is_default: bool
    pokemon: PokemonListEntry


class PokemonSpecies(TypedDict, total=False):
    evolution_chain: Dict[str, str]
    name: str
    varieties: list[Varieties]


class RawPokemon(TypedDict, total=False):
    name: str
    weight: int
    height: int
    species: PokemonListEntry
    sprites: Dict[str, Union[str, Dict[str, Dict[str, str]]]]
    types: list[RawPokemonType]


class RawTypePokemon(TypedDict):
    slot: int
    pokemon: PokemonListEntry


class RawType(TypedDict, total=False):
    name: str
    pokemon: list[RawTypePokemon]
    sprites: dict[str, dict[str, dict[str, str]]]


class PokemonList(TypedDict):
    results: list[PokemonListEntry]


class PokemonImg(TypedDict):
    default: str | None
    shiny: str | None


class PokemonPrimitive(TypedDict):
    name: str
    img: str | None


class EvolutionTree(TypedDict):
    pokemonPrimitive: PokemonPrimitive
    evolvesTo: list['EvolutionTree'] | None


class EvolutionTaskTree(TypedDict):
    task: asyncio.Task[PokemonPrimitive]
    task_tree: list['EvolutionTaskTree'] | None


class PokemonDetail(TypedDict):
    name: str
    weight: float | None
    height: int | None
    types: list[str | None]
    img: PokemonImg
    varietieTypes: list[PokemonPrimitive]
    cosmeticTypes: list[PokemonPrimitive] | None
    evolutionTree: EvolutionTree | None
