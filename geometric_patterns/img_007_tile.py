# -*- coding: utf-8 -*-
"""Generate 007 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv
import math


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    tile_side_length = param_each['tile_side_length']
    tile_margin = param_each['tile_margin']
    tile_count = param_each['tile_count']
    tile_radius = param_each['tile_radius']

    height = (tile_side_length + tile_margin) * tile_count + tile_margin
    width = height

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # background
    ctx.rectangle(0, 0, width, height)
    bkg_color = clr_cnv.rgb_dict_255_to_1(param_each['background_color'])
    ctx.set_source_rgb(bkg_color['r'], bkg_color['g'], bkg_color['b'])
    ctx.fill()

    # tiles
    color_list = list(map(clr_cnv.rgb_dict_255_to_1, param_each['color_list']))
    color_list_len = len(color_list)
    color_cnt = 0
    prev_color_x_init = 0
    for x in range(tile_margin, width, tile_side_length + tile_margin):
        if color_cnt != 0:
            color_cnt = prev_color_x_init + 1
            prev_color_x_init = color_cnt
        for y in range(tile_margin, height, tile_side_length + tile_margin):
            w = tile_side_length
            h = tile_side_length
            set_sub_path_of_rounder_rectangle(ctx, x, y, w, h, tile_radius)
            color = color_list[color_cnt % color_list_len]
            ctx.set_source_rgb(color['r'], color['g'], color['b'])
            ctx.fill_preserve()
            ctx.stroke()

            color_cnt += 1

    surface.write_to_png(_img_setting.get_img_file_path())


def set_sub_path_of_rounder_rectangle(ctx, x, y, w, h, ra):
    """Set the sub path of the rounder rectange

    Args:
        ctx (cairo.Context): The target context
        x (int): The x-coordinate
        y (int): The y-coordinate
        w (int): The width
        h (int): The hight
        ra (int): The radius
    """
    deg = math.pi / 180.0
    ctx.new_sub_path()
    ctx.arc(x + w - ra, y + ra, ra, -90 * deg, 0 * deg)
    ctx.arc(x + w - ra, y + h - ra, ra, 0 * deg, 90 * deg)
    ctx.arc(x + ra, y + h - ra, ra, 90 * deg, 180 * deg)
    ctx.arc(x + ra, y + ra, ra, 180 * deg, 270 * deg)
    ctx.close_path()


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
                    'tile_side_length',
                    'tile_margin',
                    'tile_count',
                    'tile_radius',
                    'color_list',
                    'background_color'
                ],
                'properties': {
                    'tile_side_length': {
                        'type': 'integer'
                    },
                    'tile_margin': {
                        'type': 'integer'
                    },
                    'tile_count': {
                        'type': 'integer'
                    },
                    'tile_radius': {
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
                    'background_color': {
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
                    },
                }
            }
        }
    }
}

_img_setting = ImgSetting(__file__, _input_schema)

for i in range(_img_setting.get_param_each_count()):
    gen_img()
