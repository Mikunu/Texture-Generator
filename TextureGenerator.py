from Settings import Settings
from codelogging import timeit
import numpy as np
import math
import random
import logging
from PIL import Image


def fix_out_of_bounds(size: tuple[int, int], coords: tuple[int, int]) -> tuple[int, int]:
    """
    Fix out of bounds
    :param size: image size
    :param coords: point's cords
    :return: if point in out of bounds return fixed coords else return old coords
    """
    width, height = size
    x_pos, y_pos = coords
    if x_pos >= width:
        x_pos -= width
    if x_pos < 0:
        x_pos += width
    if y_pos >= height:
        y_pos -= height
    if y_pos < 0:
        y_pos += height

    return x_pos, y_pos


def is_out_of_bounds(size: tuple[int, int], coords: tuple[int, int]) -> bool:
    width, height = size
    x_pos, y_pos = coords
    if x_pos >= width or x_pos < 0 or y_pos >= height or y_pos < 0:
        return True
    else:
        return False


def random_point(cords: tuple[int, int], radius_max: int) -> tuple[int, int]:
    """
    Get random point's coords in radius
    :param cords: x, y cords
    :param radius_max: radis
    :return: x, y cords
    """
    theta = random.uniform(0, 2 * math.pi)
    area = radius_max ** 2 * math.pi
    radius = math.sqrt(random.uniform(0, area / math.pi))
    return int(cords[0] + radius * math.cos(theta)), int(cords[1] + radius * math.sin(theta))


class TextureGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings

        # Points
        self.__parent_points_arr = None
        self.__parent_points_coordinates = None
        self.__children_points_arr = None
        self.__children_points_coordinates = None

        logging.basicConfig(level=20)

    @timeit
    def make_parents(self) -> None:
        """
        Create 2d array of parent points
        """
        if self.settings.parent_seed != -1:
            random.seed(self.settings.parent_seed)

        width, height = self.settings.size
        self.__parent_points_arr = np.full((height, width), dtype=np.uint8,
                                           fill_value=255)  # make 2d array filled with 255 (white) values
        self.__parent_points_coordinates = []
        random_offset_min, random_offset_max = self.settings.parent_random_offset
        value_min, value_max = self.settings.parent_value_range

        for i in range(int(height / self.settings.parent_distance)):
            for j in range(int(width / self.settings.parent_distance)):
                if random.random() >= self.settings.parent_spawn_chance:
                    continue
                # Set X and Y pos
                x_pos = int(
                    j * self.settings.parent_distance + random.randint(random_offset_min, random_offset_max))
                y_pos = int(
                    i * self.settings.parent_distance + random.randint(random_offset_min, random_offset_max))

                # if point exits image border it would be generated from opposite side
                x_pos, y_pos = fix_out_of_bounds(self.settings.size, (x_pos, y_pos))

                self.__parent_points_arr[y_pos, x_pos] = random.randint(value_min, value_max)
                self.__parent_points_coordinates.append((x_pos, y_pos))

    @timeit
    def make_children(self) -> None:
        """
        Generates children near parents' points
        """
        if self.__parent_points_arr is None:
            logging.critical('Parents are not initialized')
            raise TypeError

        if self.settings.children_seed is not None:
            random.seed(self.settings.children_seed)

        self.__children_points_arr = np.full(self.settings.size, dtype=np.uint8, fill_value=255)
        self.__children_points_coordinates = []

        random_mult_min, random_mult_max = self.settings.children_radius_random_range
        for cords in self.__parent_points_coordinates:
            x, y = cords
            value = self.__parent_points_arr[y, x]

            # radius = pixel value * multiplier * random value (for not being circle)
            radius: int = int(value * self.settings.children_radius_multiplier *
                              random.uniform(random_mult_min, random_mult_max))
            amount: int = int(value * self.settings.children_amount_multiplier)

            for i in range(amount):
                # n-percent of children spawn close to paren
                if i / amount < self.settings.children_close_range_distance_percent:
                    radius *= self.settings.children_close_radius_multiplier

                x_pos, y_pos = random_point((x, y), radius)
                # if point exits image border it won't be generated
                if is_out_of_bounds(self.settings.size, (x_pos, y_pos)):
                    continue

                value_min, value_max = self.settings.children_value_range
                self.__children_points_arr[y_pos, x_pos] = random.randint(value_min, value_max)
                self.__children_points_coordinates.append([(x, y), (x_pos, y_pos)])

    @timeit
    def make_image(self, arr: np.ndarray, inverted: bool = False) -> Image:
        """
        Make image from numpy array\n
        :param arr: numpy array
        :param inverted: inverted colors
        :return: Image
        """
        result_image: Image
        if inverted:
            result_image = Image.fromarray(255 - arr.astype('uint8'), 'L')
        else:
            result_image = Image.fromarray(arr.astype('uint8'), 'L')
        return result_image

    def update_params(self, settings: Settings):
        self.settings = settings

    def get_parents(self) -> np.ndarray:
        return self.__parent_points_arr

    def get_children(self) -> np.ndarray:
        return self.__children_points_arr

    def get_parent_coords(self):
        return self.__parent_points_coordinates

    def get_children_cords(self):
        return self.__children_points_coordinates
