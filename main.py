import random
import time
from TextureGenerator import TextureGenerator
from Settings import Settings
import numpy as np
import toml
from collections.abc import MutableMapping
from typing import Any
import logging
from PIL import Image, ImageFont, ImageDraw
from scipy import spatial


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


def cart2pol(x: int, y: int) -> tuple[float, float]:
    rho: float = np.sqrt(x**2 + y**2)
    phi: float = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho: int | float, phi: int | float) -> tuple[int, int]:
    x: float = rho * np.cos(phi)
    y: float = rho * np.sin(phi)
    return int(x), int(y)


if __name__ == '__main__':
    settings_data = toml.load('settings.toml')
    settings = parse_data(settings_data)
    generator = TextureGenerator(settings)
    generator.make_parents()
    generator.make_children()
    image = generator.make_image(generator.get_children(), True)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 16)
    parents_cords = generator.get_parent_coords()

    main_sequence = random.choices(parents_cords, k=10)
    print(main_sequence)
    new_par_cords = main_sequence
    old_point = new_par_cords[0]
    new_point = None
    step = 20
    max_radius = 30
    for _ in range(len(new_par_cords)):
        distance, index = spatial.KDTree(new_par_cords).query(old_point)
        new_point = new_par_cords[index]
        while distance > step:
            distance -= step
            rho, phi = cart2pol(old_point[0], old_point[1])

        draw.line((old_point, new_point), fill=192)
        new_par_cords.remove(new_point)
        old_point = new_point
    '''
    new_par_cords = parents_cords
    random_parent_coordinates = random.choice(parents_cords)
    new_par_cords.remove(random_parent_coordinates)
    old_point = random_parent_coordinates
    new_point = None
    for _ in range(len(new_par_cords)):
        
        distance, index = spatial.KDTree(new_par_cords).query(old_point)
        new_point = new_par_cords[index]
        draw.line((old_point, new_point), fill=192)
        new_par_cords.remove(new_point)
        old_point = new_point
    '''
    for children_cords in generator.get_children_cords():
        draw.line(children_cords, fill=64)
    image.show()
