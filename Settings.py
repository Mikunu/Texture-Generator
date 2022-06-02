from dataclasses import dataclass


@dataclass
class Settings:
    """Settings for generator class"""
    size: tuple[int, int]  # (width, height)

    # Parents
    parent_spawn_chance: float
    parent_random_offset: tuple[int, int]  # (min, max)
    parent_distance: int
    parent_seed: int
    parent_value_range: tuple[int, int]  # (min, max)

    # Children
    children_radius_multiplier: float
    children_radius_random_range: tuple[int, int]  # (min, max)
    children_amount_multiplier: float
    children_close_range_distance_percent: float
    children_close_radius_multiplier: float
    children_seed: int
    children_value_range: tuple[int, int]  # min, max
