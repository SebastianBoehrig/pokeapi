from typing import Dict, Union

from glom import Coalesce, glom # type: ignore

from app.types import PokemonImg


def extract_img_from_raw_pokemon_sprites(
    raw_pokemon_sprites: Dict[str, Union[str, Dict[str, Dict[str, str]]]],
) -> PokemonImg:
    return glom( # type: ignore
        raw_pokemon_sprites,
        {
            'default': Coalesce('other.official-artwork.front_default', 'front_default', default=None, skip=None),
            'shiny': Coalesce('other.official-artwork.front_shiny', 'front_shiny', default=None, skip=None),
        },
    )
