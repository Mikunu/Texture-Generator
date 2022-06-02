from TextureGenerator import TextureGenerator
from Settings import Settings
import numpy as np
from PIL import Image
import toml
from collections.abc import MutableMapping
from typing import Any


def make_image(arr: np.ndarray, inverted: bool = False) -> Image:
    """
    Make image from numpy array\n
    :param arr: numpy array
    :param inverted: inverted colors
    :return: Image
    """
    if inverted:
        return Image.fromarray(255-arr.astype('uint8'), 'L')
    else:
        return Image.fromarray(arr.astype('uint8'), 'L')


def parse_data(settings_data: MutableMapping[str, Any]) -> Settings:
    """
    Parse data from dict to dataclass\n
    :param settings_data: dict from loaded .toml file
    :return: Settings DataClass
    """
    settings = Settings(
        tuple(settings_data.get('size')),
        settings_data.get('parents').get('spawn_chance'),
        tuple(settings_data.get('parents').get('random_offset')),
        settings_data.get('parents').get('distance'),
        settings_data.get('parents').get('seed_parent'),
        tuple(settings_data.get('parents').get('parent_value_range')),
        settings_data.get('children').get('radius_multiplier'),
        tuple(settings_data.get('children').get('radius_random_range')),
        settings_data.get('children').get('children_amount_multiplier'),
        settings_data.get('children').get('close_range_distance_percent'),
        settings_data.get('children').get('close_radius_multiplier'),
        settings_data.get('children').get('seed_children'),
        tuple(settings_data.get('children').get('children_value_range'))
    )
    return settings


if __name__ == '__main__':
    settings_data = toml.load('settings.toml')
    settings = parse_data(settings_data)
    generator = TextureGenerator(settings)
    generator.make_parents()
    generator.make_children()
    image = make_image(generator.get_children(), True)
    image.show()
