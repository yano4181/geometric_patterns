# -*- coding: utf-8 -*-
"""Generate 001 images."""
import numpy as np
import cv2
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()
    height = param_each['height']
    width = param_each['width']

    color1 = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][0])
    color2 = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][1])

    img = np.zeros((height, width, 3), np.uint8)
    img[:] = color1

    radius = param_each['radius']
    unit_length = (radius * 2) + param_each['circle_margin']

    circle_x_number = width // unit_length
    circle_x_margin = width % unit_length
    circle_y_number = height // unit_length
    circle_y_margin = height % unit_length

    center_x_init = (circle_x_margin // 2) + (unit_length // 2)
    center_y_init = (circle_y_margin // 2) + (unit_length // 2)

    center_x = center_x_init
    center_y = center_y_init

    for col in range(circle_x_number):

        for row in range(circle_y_number):
            cv2.circle(img, (center_x, center_y), radius,
                       color2, -1, lineType=cv2.LINE_AA)
            center_y += unit_length

        center_x += unit_length
        center_y = center_y_init

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
                    'radius',
                    'circle_margin',
                    'color_list'
                ],
                'properties': {
                    'height': {
                        'type': 'integer'
                    },
                    'width': {
                        'type': 'integer'
                    },
                    'radius': {
                        'type': 'integer'
                    },
                    'circle_margin': {
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
