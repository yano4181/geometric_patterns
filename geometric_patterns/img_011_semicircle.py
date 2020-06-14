# -*- coding: utf-8 -*-
"""Generate 011 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv
import math


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    vertical_cnt = param_each['vertical_cnt']
    horizontal_cnt = param_each['horizontal_cnt']
    radius = param_each['radius']
    margin = param_each['margin']
    unit_length = (radius + margin) * 2

    height = vertical_cnt * unit_length
    width = horizontal_cnt * unit_length

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    color_list = list(map(clr_cnv.rgb_dict_255_to_1, param_each['color_list']))

    # background color
    ctx.rectangle(0, 0, width, height)
    ctx.set_source_rgb(color_list[0]['r'],
                       color_list[0]['g'], color_list[0]['b'])
    ctx.fill()

    # semicircles
    angle1 = (param_each['angle'] / 180) * math.pi
    angle2 = angle1 + math.pi
    to_center_length = unit_length / 2
    y_shift_percent = param_each['y_shift_percent']
    y_shift = unit_length * (y_shift_percent / 100)
    y_total_cnt = vertical_cnt if y_shift == 0 else vertical_cnt + 1
    x_shift_percent = param_each['x_shift_percent']
    x_shift = unit_length * (x_shift_percent / 100)
    x_total_cnt = horizontal_cnt + 1 if x_shift == 0 else horizontal_cnt + 2
    for y_cnt in range(y_total_cnt):
        y_coordinate = (y_cnt * unit_length) + to_center_length - y_shift

        for x_cnt in range(x_total_cnt):
            x_coordinate = (x_cnt * unit_length) + to_center_length - x_shift

            if y_cnt % 2 == 1:
                x_coordinate -= to_center_length

            ctx.arc(x_coordinate, y_coordinate, radius, angle1, angle2)
            ctx.set_source_rgb(
                color_list[1]['r'], color_list[1]['g'], color_list[1]['b'])
            ctx.fill()

    surface.write_to_png(_img_setting.get_img_file_path())


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
                    'radius',
                    'margin',
                    'vertical_cnt',
                    'horizontal_cnt',
                    'angle',
                    'x_shift_percent',
                    'y_shift_percent',
                    'color_list',
                ],
                'properties': {
                    'radius': {
                        'type': 'integer'
                    },
                    'margin': {
                        'type': 'integer'
                    },
                    'vertical_cnt': {
                        'type': 'integer'
                    },
                    'horizontal_cnt': {
                        'type': 'integer'
                    },
                    'angle': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': 359
                    },
                    'x_shift_percent': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': 100
                    },
                    'y_shift_percent': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': 100
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
                    },
                }
            }
        }
    }
}

_img_setting = ImgSetting(__file__, _input_schema)

for i in range(_img_setting.get_param_each_count()):
    gen_img()
