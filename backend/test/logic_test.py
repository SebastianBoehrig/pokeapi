from unittest.mock import patch
from fastapi import HTTPException
import pytest
from app import logic


@patch('app.logic.get_pokemon_species')
@patch('app.logic.get_pokemon')
def test_get_pokemon_primitive(pokemon_mock, species_mock):
    re_species = {'varieties': [{'is_default': True, 'pokemon': {'name': 'test_poke_default'}}]}
    re_poke = {'sprites': {'other': {'official-artwork': {'front_default': 'test_img'}}}}
    species_mock.return_value = re_species
    pokemon_mock.return_value = re_poke

    assert logic.get_pokemon_primitive('test_poke') == {'name': 'test_poke', 'img': 'test_img'}


@patch('app.logic.get_pokemon_species')
def test_get_pokemon_primitive_no_varieties(species_mock):
    species_mock.return_value = {}

    with pytest.raises(HTTPException) as excinfo:
        logic.get_pokemon_primitive('test_poke')
    assert str(excinfo.value) == '404: variety of test_poke not found, (get_pokemon_primitive)'


@patch('app.logic.get_pokemon_species')
@patch('app.logic.get_pokemon')
def test_get_pokemon_primitive_no_sprites(pokemon_mock, species_mock):
    re_species = {'varieties': [{'is_default': True, 'pokemon': {'name': 'test_poke_default'}}]}
    species_mock.return_value = re_species
    pokemon_mock.return_value = {}

    assert logic.get_pokemon_primitive('test_poke') == {'name': 'test_poke', 'img': None}


@pytest.mark.parametrize(
    'input,res',
    [
        ([{'is_default': True, 'pokemon': {'name': 'test_poke_default'}}], 'test_poke_default'),
        ([{'is_default': False, 'pokemon': {'name': 'test_poke_default'}}], None),
        ([{'is_default': False, 'pokemon': {}}], None),
        ([{'is_default': True}], None),
    ],
)
def test__extract_default_varietie_name(input, res):
    assert logic._extract_default_varietie_name(input) == res


@pytest.mark.parametrize(
    'input,res',
    [
        (
            {'other': {'official-artwork': {'front_default': 'test_img', 'front_shiny': 'test_img2'}}},
            {'default': 'test_img', 'shiny': 'test_img2'},
        ),
        (
            {'front_default': 'test_img', 'front_shiny': 'test_img2'},
            {'default': 'test_img', 'shiny': 'test_img2'},
        ),
        (
            {'other': {}},
            {'default': None, 'shiny': None},
        ),
    ],
)
def test__extract_img_from_raw_pokemon_sprites(input, res):
    assert logic._extract_img_from_raw_pokemon_sprites(input) == res
