# -*- coding: utf-8 -*-
"""Generate 015 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv
import math
import random


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    width = param_each['width']
    height = param_each['height']

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # color
    color_list = list(map(clr_cnv.rgb_dict_255_to_1, param_each['color_list']))

    # background color
    ctx.rectangle(0, 0, width, height)
    bg_color = color_list[0]
    ctx.set_source_rgb(bg_color['r'], bg_color['g'], bg_color['b'])
    ctx.fill()

    # gear
    gear_color_index = 1
    for i in range(param_each['gear_total_cnt']):
        draw_gear(ctx, random.randint(0, width),
                  random.randint(0, height), color_list[gear_color_index])

        gear_color_index += 1
        if gear_color_index >= len(color_list):
            gear_color_index = 1

    surface.write_to_png(_img_setting.get_img_file_path())


def draw_gear(ctx, xc, yc, color):
    """
    Drawing the gear

    Args:
        ctx (cairo.Context): The target context
        xc (float): The x coordinate of the gear center
        yc (float): The y coordinate of the gear center
        color (dict): The color
    """

    param_each = _img_setting.get_param_each()

    circle_radius = param_each['circle_radius']
    hole_radius = param_each['hole_radius']

    ctx.arc(xc, yc, circle_radius, 0, 2 * math.pi)
    ctx.arc(xc, yc, hole_radius, 0, 2 * math.pi)

    ctx.set_source_rgb(color['r'], color['g'], color['b'])
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.fill()

    # gear tooth
    tooth_total_num = param_each['tooth_num']
    tooth_height = param_each['tooth_height'] + circle_radius
    tooth_top_width = param_each['tooth_top_width']
    tooth_top_width_theta = (
        math.asin(tooth_top_width / (2 * tooth_height))) * 2
    tooth_bottom_width = param_each['tooth_bottom_width']
    tooth_bottom_theta = (
        math.asin(tooth_bottom_width / (2 * circle_radius))) * 2
    for tooth_cnt in range(tooth_total_num):
        theta = (2 * math.pi * tooth_cnt) / tooth_total_num
        bottom_start_theta = theta - (tooth_bottom_theta / 2)
        bottom_end_theta = theta + (tooth_bottom_theta / 2)
        top_start_theta = theta - (tooth_top_width_theta / 2)
        top_end_theta = theta + (tooth_top_width_theta / 2)
        bottom_tooth_x_start = xc + \
            (circle_radius * math.cos(bottom_start_theta))
        bottom_tooth_y_start = yc - \
            (circle_radius * math.sin(bottom_start_theta))
        bottom_tooth_x_end = xc + (circle_radius * math.cos(bottom_end_theta))
        bottom_tooth_y_end = yc - (circle_radius * math.sin(bottom_end_theta))
        top_tooth_x_start = xc + (tooth_height * math.cos(top_start_theta))
        top_tooth_y_start = yc - (tooth_height * math.sin(top_start_theta))
        top_tooth_x_end = xc + (tooth_height * math.cos(top_end_theta))
        top_tooth_y_end = yc - (tooth_height * math.sin(top_end_theta))

        ctx.move_to(bottom_tooth_x_start, bottom_tooth_y_start)
        ctx.line_to(bottom_tooth_x_end, bottom_tooth_y_end)
        ctx.line_to(top_tooth_x_end, top_tooth_y_end)
        ctx.line_to(top_tooth_x_start, top_tooth_y_start)
        ctx.fill()


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
                    'width',
                    'height',
                    'hole_radius',
                    'circle_radius',
                    'tooth_num',
                    'tooth_top_width',
                    'tooth_bottom_width',
                    'tooth_height',
                    'gear_total_cnt',
                    'color_list',
                ],
                'properties': {
                    'width': {
                        'type': 'integer'
                    },
                    'height': {
                        'type': 'integer'
                    },
                    'hole_radius': {
                        'type': 'integer'
                    },
                    'circle_radius': {
                        'type': 'integer'
                    },
                    'tooth_num': {
                        'type': 'integer'
                    },
                    'tooth_top_width': {
                        'type': 'integer'
                    },
                    'tooth_bottom_width': {
                        'type': 'integer'
                    },
                    'tooth_height': {
                        'type': 'integer'
                    },
                    'gear_total_cnt': {
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
