# -*- coding: utf-8 -*-
"""Convert color."""


def rgb_dict_to_bgr_list(rgb_color):
    """Convert rgb color dict to bgr list.

    Args:
        rgb_color (dict): color with rgb

    Returns:
        list: bgr list
    """
    return [rgb_color['b'], rgb_color['g'], rgb_color['r']]


def rgb_dict_255_to_1(rgb_color):
    """Convert rgb color dict value range from 0-255 to 0-1.

    Args:
        rgb_color (dict): rgb color with 0-255

    Returns:
        dict: rgb color with 0-1
    """
    return {
        'r': rgb_color['r'] / 255,
        'g': rgb_color['g'] / 255,
        'b': rgb_color['b'] / 255
    }
