from unittest.mock import AsyncMock, call, patch

from app.logic import get_pokemon_primitive_of_type


@patch('app.logic.get_pokemon_primitive_of_type.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_primitive_of_type.get_pokemon', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_primitive_of_type.get_type', new_callable=AsyncMock)
async def test_get_pokemon_primitive_of_type(
    get_type_mock, get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, async_client
):
    get_type_mock.return_value = {
        'pokemon': [{'pokemon': {'name': 'p1'}}, {'pokemon': {'name': 'p2'}}, {'pokemon': {'name': 'p3'}}]
    }
    get_pokemon_mock.side_effect = [
        {'name': 'poke_name_1', 'sprites': {'sprites_p1'}},
        {'name': 'poke_name_2', 'sprites': {'sprites_p2'}},
        {'name': 'poke_name_3', 'sprites': {'sprites_p3'}},
    ]
    extract_img_from_raw_pokemon_sprites_mock.side_effect = [
        {'default': 'poke_img_1'},
        {'default': 'poke_img_2'},
        {'default': 'poke_img_3'},
    ]

    assert await get_pokemon_primitive_of_type.get_pokemon_primitive_of_type('test_type', async_client) == [
        {
            'name': 'poke_name_1',
            'img': 'poke_img_1',
        },
        {
            'name': 'poke_name_2',
            'img': 'poke_img_2',
        },
        {
            'name': 'poke_name_3',
            'img': 'poke_img_3',
        },
    ]
    calls_get_pokemon = [call('p1', async_client), call('p2', async_client), call('p3', async_client)]
    get_pokemon_mock.assert_has_awaits(calls_get_pokemon)
    calls_extract_img = [call({'sprites_p1'}), call({'sprites_p2'}), call({'sprites_p3'})]
    extract_img_from_raw_pokemon_sprites_mock.assert_has_calls(calls_extract_img)


@patch('app.logic.get_pokemon_primitive_of_type.get_type', new_callable=AsyncMock)
async def test_get_pokemon_primitive_of_type_no_pokemons(get_type_mock, async_client):
    get_type_mock.return_value = {'pokemon': []}

    assert await get_pokemon_primitive_of_type.get_pokemon_primitive_of_type('test_type', async_client) == []


@patch('app.logic.get_pokemon_primitive_of_type.get_type', new_callable=AsyncMock)
async def test_get_pokemon_primitive_of_type_no_pokemon_names_in_types(get_type_mock, async_client):
    get_type_mock.return_value = {'pokemon': [{'pokemon': {}}, {'pokemon': {'name': None}}]}

    assert await get_pokemon_primitive_of_type.get_pokemon_primitive_of_type('test_type', async_client) == []


@patch('app.logic.get_pokemon_primitive_of_type.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_primitive_of_type.get_pokemon', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_primitive_of_type.get_type', new_callable=AsyncMock)
async def test_get_pokemon_primitive_of_type_no_individual_pokemon_name(
    get_type_mock, get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, async_client
):
    get_type_mock.return_value = {'pokemon': [{'pokemon': {'name': 'p1'}}]}
    get_pokemon_mock.return_value = {'name': None, 'sprites': {'sprites_p1'}}
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img_1'}

    assert await get_pokemon_primitive_of_type.get_pokemon_primitive_of_type('test_type', async_client) == [
        {
            'name': '',
            'img': 'poke_img_1',
        }
    ]
