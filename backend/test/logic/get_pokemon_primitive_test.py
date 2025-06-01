from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import HTTPException

from app.logic import get_pokemon_primitive


@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client


@patch('app.logic.get_pokemon_primitive.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_primitive.get_pokemon', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_primitive.get_pokemon_species', new_callable=AsyncMock)
async def test_get_pokemon_primitive(
    get_pokemon_species_mock, get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, async_client
):
    get_pokemon_species_mock.return_value = {
        'name': 'poke_name',
        'varieties': [{'is_default': True, 'pokemon': {'name': 'default_var_name'}}],
    }
    get_pokemon_mock.return_value = {'sprites': {'sprites_object'}}
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img'}

    assert await get_pokemon_primitive.get_pokemon_primitive('testpoke', async_client) == {
        'name': 'poke_name',
        'img': 'poke_img',
    }
    get_pokemon_mock.assert_awaited_once_with('default_var_name', async_client)
    extract_img_from_raw_pokemon_sprites_mock.assert_called_once_with({'sprites_object'})


@pytest.mark.parametrize(
    'variety_return, error',
    [
        ([], 'variety of testpoke not found, (get_pokemon_primitive)'),
        ([{'is_default': False}], 'default varietie of testpoke not found, (get_pokemon_primitive)'),
    ],
)
@patch('app.logic.get_pokemon_primitive.get_pokemon_species', new_callable=AsyncMock)
async def test_get_pokemon_primitive_404(get_pokemon_species_mock, async_client, variety_return, error):
    get_pokemon_species_mock.return_value = {
        'name': 'poke_name',
        'varieties': variety_return,
    }

    with pytest.raises(HTTPException) as excinfo:
        print(await get_pokemon_primitive.get_pokemon_primitive('testpoke', async_client))
    assert str(excinfo.value) == f'404: {error}'


@patch('app.logic.get_pokemon_primitive.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_primitive.get_pokemon', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_primitive.get_pokemon_species', new_callable=AsyncMock)
async def test_get_pokemon_primitive_no_name(
    get_pokemon_species_mock, get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, async_client
):
    get_pokemon_species_mock.return_value = {  # No name here
        'varieties': [{'is_default': True, 'pokemon': {'name': 'default_var_name'}}]
    }
    get_pokemon_mock.return_value = {'sprites': {'sprites_object'}}
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img'}

    assert await get_pokemon_primitive.get_pokemon_primitive('testpoke', async_client) == {
        'name': 'testpoke',
        'img': 'poke_img',
    }
