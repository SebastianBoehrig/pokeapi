from app import pokeapi_requests, config
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def mock_requests():
    with patch('app.pokeapi_requests.requests') as mock_requests:
        yield mock_requests


def test_api_online(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.api_online() is True
    mock_requests.get.assert_called_with(config.POKEAPI_BASE_URL)


def test_api_online_false(mock_requests):
    mock_response = MagicMock(status_code=404)
    mock_requests.get.return_value = mock_response

    assert not pokeapi_requests.api_online()
    mock_requests.get.assert_called_with(config.POKEAPI_BASE_URL)


def test_get_all_pokemon(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {'results': [{'name': 'bulbasaur', 'url': 'ignore'}, {'name': 'ivysaur'}]}
    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_all_pokemon() == {'bulbasaur', 'ivysaur'}
    mock_requests.get.assert_called_with(f'{config.POKEAPI_POKEMON_URL}/{config.HIGH_LIMIT}')


@pytest.mark.parametrize(
    'fkt',
    [(pokeapi_requests.get_all_pokemon), (pokeapi_requests.get_all_pokemon_species), (pokeapi_requests.get_all_types)],
)
def test_all_failiure(fkt, mock_requests):
    mock_response = MagicMock(status_code=403)
    mock_requests.get.return_value = mock_response

    assert fkt() is None


@pytest.mark.parametrize(
    'fkt',
    [
        (pokeapi_requests.get_pokemon_of_species),
        (pokeapi_requests.get_pokemon_of_type),
        (pokeapi_requests.get_single_pokemon),
    ],
)
def test_all_failiure_param(fkt, mock_requests):
    mock_response = MagicMock(status_code=403)
    mock_requests.get.return_value = mock_response

    assert fkt('water') is None


def test_get_all_pokemon_species(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {'results': [{'name': 'bulbasaur', 'url': 'ignore'}, {'name': 'ivysaur'}]}
    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_all_pokemon_species() == {'bulbasaur', 'ivysaur'}
    mock_requests.get.assert_called_with(f'{config.POKEAPI_SPECIES_URL}/{config.HIGH_LIMIT}')


def test_get_pokemon_of_species(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {
        'varieties': [
            {'is_default': False, 'pokemon': {'name': 'aegislash-shield', 'url': 'ignore'}},
            {'is_default': True, 'pokemon': {'name': 'aegislash-blade'}},
        ]
    }
    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_pokemon_of_species('aegislash') == {
        'default': 'aegislash-blade',
        'other': ['aegislash-shield'],
    }
    mock_requests.get.assert_called_with(f'{config.POKEAPI_SPECIES_URL}/aegislash/{config.HIGH_LIMIT}')


def test_get_pokemon_of_species_empty(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {'varieties': []}
    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_pokemon_of_species('aegislash') is None
    mock_requests.get.assert_called_with(f'{config.POKEAPI_SPECIES_URL}/aegislash/{config.HIGH_LIMIT}')


def test_get_single_pokemon(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {
        'name': 'scyther',
        'weight': 560,
        'height': 15,
        'types': [{'slot': 1, 'type': {'name': 'bug', 'url': 'ignore'}}, {'type': {'name': 'flying'}}],
        'sprites': {'other': {'official-artwork': {'front_default': 'default_url', 'front_shiny': 'shiny_url'}}},
    }

    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_single_pokemon('ditto') == {
        'name': 'scyther',
        'weight': 560,
        'height': 15,
        'types': {'bug', 'flying'},
        'img': {'default': 'default_url', 'shiny': 'shiny_url'},
    }
    mock_requests.get.assert_called_with(f'{config.POKEAPI_POKEMON_URL}/ditto')


def test_get_single_pokemon_no_official_art(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {
        'name': 'scyther',
        'weight': 560,
        'height': 15,
        'types': [{'type': {'name': 'bug'}}],
        'sprites': {'front_default': 'default_url', 'front_shiny': 'shiny_url'},
    }

    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_single_pokemon('ditto') == {
        'name': 'scyther',
        'weight': 560,
        'height': 15,
        'types': {'bug'},
        'img': {'default': 'default_url', 'shiny': 'shiny_url'},
    }
    mock_requests.get.assert_called_with(f'{config.POKEAPI_POKEMON_URL}/ditto')


def test_get_all_types(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {'results': [{'name': 'water', 'url': 'ignore'}, {'name': 'steel'}]}

    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_all_types() == {'water', 'steel'}
    mock_requests.get.assert_called_with(f'{config.POKEAPI_TYPE_URL}/{config.HIGH_LIMIT}')


def test_get_pokemon_of_type(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {
        'pokemon': [{'pokemon': {'name': 'wartortle', 'url': 'ignore'}, 'slot': 1}, {'pokemon': {'name': 'seadra'}}]
    }

    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_pokemon_of_type('water') == {'wartortle', 'seadra'}
    mock_requests.get.assert_called_with(f'{config.POKEAPI_TYPE_URL}/water/{config.HIGH_LIMIT}')
