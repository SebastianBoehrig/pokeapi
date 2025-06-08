from unittest.mock import AsyncMock, call, patch

from app.logic import get_pokemon_detail

# evolution tests for get_pokemon_detail


@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_no_evolution_url(
    get_pokemon_mock, extract_img_from_raw_pokemon_sprites_mock, get_pokemon_species_mock, async_client
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {'evolution_chain': {'url': None}}

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('evolutionTree') is None


@patch('app.logic.get_pokemon_detail.get_pokemon_primitive', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.get_evolution_chain', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_evolution_tree(
    get_pokemon_mock,
    extract_img_from_raw_pokemon_sprites_mock,
    get_pokemon_species_mock,
    get_evolution_chain_mock,
    get_pokemon_primitive_mock,
    async_client,
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {'evolution_chain': {'url': 'evo_url'}}
    get_evolution_chain_mock.return_value = {
        'species': {'name': 'evo_base_p'},
        'evolves_to': [
            {
                'species': {'name': 'evo_mid_p_1'},
                'evolves_to': [
                    {
                        'species': {'name': 'evo_end_p_1'},
                        'evolves_to': [],
                    },
                    {
                        'species': {'name': 'evo_end_p_2'},
                        'evolves_to': [],
                    },
                ],
            },
            {
                'species': {'name': 'evo_mid_p_2'},
                'evolves_to': [
                    {
                        'species': {'name': 'evo_end_p_3'},
                        'evolves_to': [],
                    },
                    {
                        'species': {'name': 'evo_end_p_4'},
                        'evolves_to': [],
                    },
                ],
            },
        ],
    }
    get_pokemon_primitive_mock.side_effect = [
        {'base-primitive'},
        {'mid-primitive_1'},
        {'end-primitive_1'},
        {'end-primitive_2'},
        {'mid-primitive_2'},
        {'end-primitive_3'},
        {'end-primitive_4'},
    ]

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('evolutionTree') == {
        'pokemonPrimitive': {'base-primitive'},
        'evolvesTo': [
            {
                'pokemonPrimitive': {'mid-primitive_1'},
                'evolvesTo': [
                    {
                        'pokemonPrimitive': {'end-primitive_1'},
                        'evolvesTo': None,
                    },
                    {
                        'pokemonPrimitive': {'end-primitive_2'},
                        'evolvesTo': None,
                    },
                ],
            },
            {
                'pokemonPrimitive': {'mid-primitive_2'},
                'evolvesTo': [
                    {
                        'pokemonPrimitive': {'end-primitive_3'},
                        'evolvesTo': None,
                    },
                    {
                        'pokemonPrimitive': {'end-primitive_4'},
                        'evolvesTo': None,
                    },
                ],
            },
        ],
    }
    get_evolution_chain_mock.assert_awaited_once_with('evo_url', async_client)
    calls = [
        call('evo_base_p', async_client),
        call('evo_mid_p_1', async_client),
        call('evo_end_p_1', async_client),
        call('evo_end_p_2', async_client),
        call('evo_mid_p_2', async_client),
        call('evo_end_p_3', async_client),
        call('evo_end_p_4', async_client),
    ]
    get_pokemon_primitive_mock.assert_has_awaits(calls)


@patch('app.logic.get_pokemon_detail.get_evolution_chain', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_no_evolvesTo(
    get_pokemon_mock,
    extract_img_from_raw_pokemon_sprites_mock,
    get_pokemon_species_mock,
    get_evolution_chain_mock,
    async_client,
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {'evolution_chain': {'url': 'evo_url'}}
    get_evolution_chain_mock.return_value = {'species': {'name': 'evo_base_p'}}

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('evolutionTree') is None


@patch('app.logic.get_pokemon_detail._resolve_tree_recursive', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.get_evolution_chain', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.get_pokemon_species', new_callable=AsyncMock)
@patch('app.logic.get_pokemon_detail.extract_img_from_raw_pokemon_sprites')
@patch('app.logic.get_pokemon_detail.get_pokemon', new_callable=AsyncMock)
async def test_get_pokemon_detail_evolution_tree_error(
    get_pokemon_mock,
    extract_img_from_raw_pokemon_sprites_mock,
    get_pokemon_species_mock,
    get_evolution_chain_mock,
    _resolve_tree_recursive_mock,
    async_client,
):
    get_pokemon_mock.return_value = {
        'name': 'poke_name',
        'types': [],
        'sprites': {'sprites_obj'},
        'species': {'name': 'p_species'},
    }
    extract_img_from_raw_pokemon_sprites_mock.return_value = {'default': 'poke_img', 'shiny': 'poke_img_shiny'}
    get_pokemon_species_mock.return_value = {'evolution_chain': {'url': 'evo_url'}}
    get_evolution_chain_mock.return_value = {
        'species': {'name': 'evo_base_p'},
        'evolves_to': [
            {
                'species': {'name': 'evo_mid_p_1'},
                'evolves_to': [],
            }
        ],
    }
    _resolve_tree_recursive_mock.side_effect = Exception('testing handeling potential errors')

    assert (await get_pokemon_detail.get_pokemon_detail('testpoke', async_client)).get('evolutionTree') is None
