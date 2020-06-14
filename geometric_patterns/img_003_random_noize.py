# -*- coding: utf-8 -*-
"""Generate 003 images."""
import numpy as np
import cv2
from common.setting import ImgSetting


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()
    side_length = param_each['side_length']

    img = np.random.randint(0, 255, (side_length, side_length, 3), np.uint8)

    division_number = param_each['division_number']
    unit_length = side_length // division_number
    if unit_length <= 1:
        cv2.imwrite(_img_setting.get_img_file_path(), img)
        return

    for x in range(0, side_length, unit_length):
        for y in range(0, side_length, unit_length):
            img[x:x + unit_length, y:y +
                unit_length] = np.random.randint(0, 255, 3, np.uint8)

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
                    'side_length',
                    'division_number'
                ],
                'properties': {
                    'side_length': {
                        'type': 'integer'
                    },
                    'division_number': {
                        'type': 'integer'
                    },
                }
            }
        }
    }
}

_img_setting = ImgSetting(__file__, _input_schema)

for i in range(_img_setting.get_param_each_count()):
    gen_img()
