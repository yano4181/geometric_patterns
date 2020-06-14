# -*- coding: utf-8 -*-
"""Generate 004 images."""
import numpy as np
import cv2
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    step_count = param_each['step_count']
    step_width = param_each['step_width']

    height = step_count * step_width
    width = step_count * step_width

    img = np.zeros((height, width, 3), np.uint8)
    img[:] = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][0])

    color_selector = 0
    line_color_1 = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][1])
    line_color_2 = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][2])
    line_width = param_each['line_width']
    for y in range(0, height, step_width):
        for x in range(0, width, step_width):
            color_selector += 1
            line_color = line_color_1 if (
                color_selector % 2) == 0 else line_color_2
            cv2.line(img, (x, y), (x + step_width, y + step_width),
                     line_color, line_width, cv2.LINE_AA)

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
                    'line_width',
                    'step_count',
                    'step_width',
                    'color_list'
                ],
                'properties': {
                    'line_width': {
                        'type': 'integer'
                    },
                    'step_count': {
                        'type': 'integer'
                    },
                    'step_width': {
                        'type': 'integer'
                    },
                    'color_list': {
                        'type': 'array',
                        'minItems': 3,
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
