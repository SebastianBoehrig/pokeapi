from unittest.mock import MagicMock, patch

import pytest
import httpx
from fastapi import HTTPException

from app import config, pokeapi_requests


@pytest.fixture
def client():
    with httpx.Client() as client:
        yield client


def test_api_online(httpx_mock, client):
    httpx_mock.add_response(status_code=200)

    assert pokeapi_requests.api_online(client) is True
    assert httpx_mock.get_requests()[0].url == config.POKEAPI_BASE_URL


def test_api_online_false(httpx_mock, client):
    httpx_mock.add_response(status_code=404)

    assert not pokeapi_requests.api_online(client)
    assert httpx_mock.get_requests()[0].url == config.POKEAPI_BASE_URL


async def test_get_evolution_chain(httpx_mock, async_client):
    httpx_mock.add_response(
        url='http://pokemon/123',
        json={'chain': {'test': 'chain'}},
        status_code=200,
    )

    assert await pokeapi_requests.get_evolution_chain('http://pokemon/123', async_client) == {'test': 'chain'}
    assert len(httpx_mock.get_requests()) == 1


@pytest.mark.parametrize(
    'fkt,param,msg',
    [
        (pokeapi_requests.get_pokemon_species, True, 'test not found, (get_pokemon_species)'),
        (pokeapi_requests.get_pokemon, True, 'test not found, (get_pokemon)'),
        (pokeapi_requests.get_type, True, 'test not found, (get_type)'),
        (pokeapi_requests.get_all_types, False, 'pokemon types list not found, (get_all_types)'),
    ],
)
async def test_404(fkt, param, msg, httpx_mock, async_client):
    httpx_mock.add_response(status_code=404)

    with pytest.raises(HTTPException) as excinfo:
        if param:
            print(await fkt('test', async_client))
        else:
            print(await fkt(async_client))
    assert str(excinfo.value) == f'404: {msg}'


async def test_get_evolution_chain_404(httpx_mock, async_client):
    httpx_mock.add_response(status_code=404)

    with pytest.raises(HTTPException) as excinfo:
        print(await pokeapi_requests.get_evolution_chain('http://test', async_client))
    assert str(excinfo.value) == '404: evolution not found: http://test, (get_evolution_chain)'
