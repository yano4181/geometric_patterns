# -*- coding: utf-8 -*-
"""Generate 010 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv
import random


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    square_side_length = param_each['square_side_length']
    square_cnt = param_each['square_cnt']

    height = square_side_length * square_cnt
    width = height

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # background color (white)
    ctx.rectangle(0, 0, width, height)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()

    color_list = list(map(clr_cnv.rgb_dict_255_to_1, param_each['color_list']))
    color_list_cnt = len(color_list)
    for x_cnt in range(0, square_cnt):
        for y_cnt in range(0, square_cnt):
            x_base = x_cnt * square_side_length
            y_base = y_cnt * square_side_length
            top_left = {'x': x_base, 'y': y_base}
            bottom_left = {'x': x_base, 'y': y_base + square_side_length}
            center = {'x': x_base + (square_side_length / 2),
                      'y': y_base + (square_side_length / 2)}
            top_right = {'x': x_base + square_side_length, 'y': y_base}
            bottom_right = {'x': x_base + square_side_length,
                            'y': y_base + square_side_length}
            drawPolygon(ctx, (top_left, bottom_left, center),
                        color_list[random.randrange(color_list_cnt)])
            drawPolygon(ctx, (top_right, bottom_right, center),
                        color_list[random.randrange(color_list_cnt)])
            drawPolygon(ctx, (top_left, top_right, center),
                        color_list[random.randrange(color_list_cnt)])
            drawPolygon(ctx, (bottom_left, bottom_right, center),
                        color_list[random.randrange(color_list_cnt)])

    surface.write_to_png(_img_setting.get_img_file_path())


def drawPolygon(ctx, coodinates, color):
    for ind, coodinate in enumerate(coodinates):
        x = coodinate['x']
        y = coodinate['y']
        if ind == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

    ctx.set_source_rgb(color['r'], color['g'], color['b'])
    ctx.fill()

    ctx.stroke()


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
                    'square_side_length',
                    'square_cnt',
                    'color_list',
                ],
                'properties': {
                    'square_side_length': {
                        'type': 'integer'
                    },
                    'square_cnt': {
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
                    },
                }
            }
        }
    }
}

_img_setting = ImgSetting(__file__, _input_schema)

for i in range(_img_setting.get_param_each_count()):
    gen_img()
