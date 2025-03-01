from fastapi import HTTPException
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


def test_get_evolution_chain(mock_requests):
    mock_response = MagicMock(status_code=200)
    mock_response.json = lambda: {'chain': {'test': 'chain'}}
    mock_requests.get.return_value = mock_response

    assert pokeapi_requests.get_evolution_chain('pokemon') == {'test': 'chain'}


@pytest.mark.parametrize(
    'fkt,param,msg',
    [
        (pokeapi_requests.get_pokemon_species, True, 'test not found, (get_pokemon_species)'),
        (pokeapi_requests.get_pokemon, True, 'test not found, (get_pokemon)'),
        (pokeapi_requests.get_type, True, 'test not found, (get_type)'),
        (pokeapi_requests.get_evolution_chain, True, 'evolution not found: test, (get_evolution_chain)'),
        (pokeapi_requests.get_all_types, False, 'pokemon types list not found, (get_all_types)'),
        (pokeapi_requests.get_all_pokemon_species, False, 'pokemon species list not found, (get_all_pokemon_species)'),
    ],
)
def test_404(fkt, param, msg, mock_requests):
    mock_response = MagicMock(status_code=404)
    mock_requests.get.return_value = mock_response

    with pytest.raises(HTTPException) as excinfo:
        if param:
            print(fkt('test'))
        else:
            print(fkt())
    assert str(excinfo.value) == f'404: {msg}'
