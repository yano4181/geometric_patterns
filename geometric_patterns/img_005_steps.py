# -*- coding: utf-8 -*-
"""Generate 005 images."""
import numpy as np
import cv2
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    step_length = param_each['step_length']
    step_width = param_each['step_width']

    line_width = param_each['line_width']
    line_adjustment = -(-line_width // 2) + 1

    height = step_length * step_width + line_adjustment
    width = step_length * step_width + line_adjustment

    img = np.zeros((height, width, 3), np.uint8)
    img[:] = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][0])

    line_color = clr_cnv.rgb_dict_to_bgr_list(param_each['color_list'][1])
    for step_count in range(0, step_length, 1):
        x_start, x_end, y_start, y_end = get_coordinates(
            step_count, line_adjustment)

        cv2.line(img, (x_start, y_start), (x_end, y_start),
                 line_color, line_width, cv2.LINE_AA)
        cv2.line(img, (x_end, y_start), (x_end, y_end),
                 line_color, line_width, cv2.LINE_AA)

    cv2.imwrite(_img_setting.get_img_file_path(), img)


def get_coordinates(step_count, line_adjustment):
    """Get the x y coordinates.

    Args:
        step_count (int): The step count
        line_adjustment (int): The line adjustment
    Returns:
        tuple: The coodinates of x start, x end, y start, and y end
    """
    param_each = _img_setting.get_param_each()
    step_length = param_each['step_length']
    step_width = param_each['step_width']
    direction = param_each['direction']
    x_start, x_end, y_start, y_end = (0, 0, 0, 0)
    if direction:
        x_start = step_count * step_width
        y_start = step_count * step_width + line_adjustment
        x_end = x_start + step_width
        y_end = y_start + step_width
    else:
        x_start = step_count * step_width
        y_start = (step_length - step_count) * step_width
        x_end = x_start + step_width
        y_end = y_start - step_width

    return (x_start, x_end, y_start, y_end)


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
                    'step_length',
                    'step_width',
                    'direction',
                    'color_list'
                ],
                'properties': {
                    'line_width': {
                        'type': 'integer'
                    },
                    'step_length': {
                        'type': 'integer'
                    },
                    'step_width': {
                        'type': 'integer'
                    },
                    'direction': {
                        'type': 'boolean'
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
