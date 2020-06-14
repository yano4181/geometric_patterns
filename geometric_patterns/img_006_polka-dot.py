# -*- coding: utf-8 -*-
"""Generate 006 images."""
import numpy as np
import cv2
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""

    param_each = _img_setting.get_param_each()
    height = param_each['height']
    width = param_each['width']

    unit_length = param_each['unit_length']
    radius = param_each['radius']

    even_x_total_length = width - (width % unit_length)
    odd_x_total_length = even_x_total_length - (unit_length // 2)

    even_x_init = ((width - even_x_total_length) // 2) + (unit_length // 2)
    odd_x_init = even_x_init + (unit_length // 2)

    y_total_length = height - (height % unit_length)
    y_init = ((height - y_total_length) // 2) + (unit_length // 2)

    img = np.zeros((height, width, 3), np.uint8)
    img[:] = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][0])

    dot_color = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][1])

    for odd_x in range(odd_x_init, odd_x_total_length, unit_length):
        for y_4_odd_x in range(y_init, y_total_length, unit_length):
            cv2.circle(img, (odd_x, y_4_odd_x), radius,
                       dot_color, -1, lineType=cv2.LINE_AA)

    for even_x in range(even_x_init, even_x_total_length, unit_length):
        for y_4_even_x in range(y_init + (unit_length // 2), y_total_length,
                                unit_length):
            cv2.circle(img, (even_x, y_4_even_x), radius,
                       dot_color, -1, lineType=cv2.LINE_AA)

    cv2.imwrite(_img_setting.get_img_file_path(), img)


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
                    'height',
                    'width',
                    'unit_length',
                    'radius',
                    'color_list'
                ],
                'properties': {
                    'height': {
                        'type': 'integer'
                    },
                    'width': {
                        'type': 'integer'
                    },
                    'unit_length': {
                        'type': 'integer'
                    },
                    'radius': {
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
