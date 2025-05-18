from app.logic.helpers import extract_img_from_raw_pokemon_sprites
import pytest

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
def test_extract_img_from_raw_pokemon_sprites(input, res):
    assert extract_img_from_raw_pokemon_sprites(input) == res