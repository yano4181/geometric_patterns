# -*- coding: utf-8 -*-
"""Generate 002 images."""
import numpy as np
import cv2
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    triangle_base = param_each['triangle_base']
    triangle_base_half = round(triangle_base / 2)
    triangle_height = param_each['triangle_height']

    triangle_base_count = param_each['triangle_base_count']

    x_total_length = triangle_base * triangle_base_count
    y_total_length = triangle_height * (x_total_length // triangle_height)

    color1 = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][0])
    color2 = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][1])

    img = np.zeros((y_total_length, x_total_length, 3), np.uint8)
    img[:] = color1

    x_init = 0
    y_init = 0

    y_count = 0
    for y_coordinate in range(y_init, y_total_length, triangle_height):
        y_count += 1

        if y_count % 2 == 0:
            pts = get_pts(x_init - triangle_base_half, y_coordinate,
                          triangle_height, triangle_base, triangle_base_half)
            cv2.fillPoly(img, pts, color2)

        for x_coordinate in range(x_init, x_total_length, triangle_base):
            if y_count % 2 == 0:
                x_coordinate += triangle_base_half

            pts = get_pts(x_coordinate, y_coordinate,
                          triangle_height, triangle_base, triangle_base_half)
            cv2.fillPoly(img, pts, color2)

    cv2.imwrite(_img_setting.get_img_file_path(), img)


def get_pts(x_coordinate, y_coordinate, triangle_height, triangle_base,
            triangle_base_half):
    """Get the triangle plots.

    Args:
        x_coordinate (int): The x coordinate
        y_coordinate (int): The y coordinate
        triangle_height(int): The triangle height
        triangle_base(int): The triangle base width
        triangle_base_half(int): The triangle base half width
    """
    pts = np.array(
        [[x_coordinate, y_coordinate + triangle_height],
         [x_coordinate + triangle_base,
          y_coordinate + triangle_height],
            [x_coordinate + triangle_base_half, y_coordinate]],
        np.int32)
    return [pts]


_input_schema = {
    'type': 'object',
    'required': [
        'each'
    ],
    'properties': {
        'each': {
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'object',
                'required': [
                    'triangle_base_count',
                    'triangle_base',
                    'triangle_height',
                    'color_list'
                ],
                'properties': {
                    'triangle_base_count': {
                        'type': 'integer'
                    },
                    'triangle_base': {
                        'type': 'integer'
                    },
                    'triangle_height': {
                        'type': 'integer'
                    },
                    'color_list': {
                        'type': 'array',
                        'minItems': 2,
                        'items': {
                            'type': 'object',
                            'required': ['r', 'g', 'b'],
                            'properties': {
                                'r': {
                                    'type': 'integer',
                                    'minimum': 0,
                                    'maximum': 255
                                },
                                'g': {
                                    'type': 'integer',
                                    'minimum': 0,
                                    'maximum': 255
                                },
                                'b': {
                                    'type': 'integer',
                                    'minimum': 0,
                                    'maximum': 255
                                },
                            }
                        }
                    }
                }
            }
        }
    }
}

_img_setting = ImgSetting(__file__, _input_schema)

for i in range(_img_setting.get_param_each_count()):
    gen_img()
