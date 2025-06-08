from unittest.mock import AsyncMock, call, patch

import pytest
from fastapi import HTTPException

from app.logic import get_pokemon_detail


@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, get_pokemon_species_mock, async_client
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {}

    assert await get_pokemon_detail.get_pokemon_detail('testpoke', async_client) == {
        'name': 'poke_name',
        'weight': None,
        'height': None,
        'types': [],
        'img': {'default': 'poke_img', 'shiny': 'poke_img_shiny'},
        'varietieTypes': [],
        'cosmeticTypes': None,
        'evolutionTree': None,
    }
    get_pokemon_mock.assert_awaited_once_with('testpoke', async_client)
    extract_img_from_raw_pokemon_sprites_mock.assert_called_once_with({'sprites_obj'})
    get_pokemon_species_mock.assert_awaited_once_with('p_species', async_client)


@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_types(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, get_pokemon_species_mock, async_client
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [{'type': {'name': 't1'}}, {'type': {'name': 't2'}}],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {}
    get_pokemon_species_mock.return_value = {}

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('types') == ['t1', 't2']


@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_data_points(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, get_pokemon_species_mock, async_client
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'weight': 100,
        'height': 100,
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {}
    get_pokemon_species_mock.return_value = {}

    result = await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)
    assert result.get('weight') == 10
    assert result.get('height') == 1000


@pytest.mark.parametrize(
    'species_dict',
    [
        ({'species': {'name': None}}),
        ({'species': {}}),
        ({}),
    ],
)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_no_species_name(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, async_client, species_dict
):
    get_pokemon_mock.return_value = {'name': 'poke_name', 'types': [], 'sprites': {'sprites_obj'}, **species_dict}
    extract_img_from_raw_pokemon_sprites_mock.return_value = {}

    with pytest.raises(HTTPException) as excinfo:
        print(await get_pokemon_detail.get_pokemon_detail('testpoke', async_client))
    assert str(excinfo.value) == '404: species of testpoke not found, (get_pokemon_detail)'


@pytest.mark.parametrize(
    'variety_name_dict,result_name',
    [
        ({}, ''),
        ({'name': 'poke_var'}, 'poke_var'),
    ],
)
@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_varieties_green(
    get_pokemon_mock,
    extract_img_from_raw_pokemon_sprites_mock,
    get_pokemon_species_mock,
    async_client,
    variety_name_dict,
    result_name,
):
    get_pokemon_mock.side_effect = [
        {  # original pokemon
            'name': 'poke_name',
            'types': [],
            'sprites': {'sprites_obj_poke'},
            'species': {'name': 'p_species'},
        },
        {  # variety
            **variety_name_dict,
            'sprites': {'sprites_obj_var'},
        },
    ]
    extract_img_from_raw_pokemon_sprites_mock.side_effect = [
        {'default': 'poke_img', 'shiny': 'poke_img_shiny'},  # original pokemon
        {'default': 'var_img'},  # variety
    ]
    get_pokemon_species_mock.return_value = {'varieties': [{'pokemon': {'name': 'testvar'}}]}

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('varietieTypes') == [
        {'name': result_name, 'img': 'var_img'}
    ]
    calls_get_pokemon = [call('testpoke', async_client), call('testvar', async_client)]
    get_pokemon_mock.assert_has_awaits(calls_get_pokemon)
    calls_get_pokemon = [call({'sprites_obj_poke'}), call({'sprites_obj_var'})]
    extract_img_from_raw_pokemon_sprites_mock.assert_has_calls(calls_get_pokemon)


@pytest.mark.parametrize(
    'varieties_dict',
    [
        ({}),
        ({'pokemon': None}),
        ({'pokemon': {}}),
        ({'pokemon': {'name': 'poke_name'}}),
    ],
)
@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_varieties_red(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, get_pokemon_species_mock, async_client, varieties_dict
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {'varieties': [varieties_dict]}

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('varietieTypes') == []


@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_no_poke_name(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, get_pokemon_species_mock, async_client
):
    get_pokemon_mock.return_value = {
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {}

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('name') == 'testpoke'
