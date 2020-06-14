# -*- coding: utf-8 -*-
"""Generate 014 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv
import math


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()
    unit_length = param_each['unit_length']
    horizontal_unit_cnt = param_each['horizontal_unit_cnt']
    vartical_unit_cnt = param_each['vartical_unit_cnt']

    width = horizontal_unit_cnt * unit_length
    height = vartical_unit_cnt * unit_length

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # background color
    ctx.rectangle(0, 0, width, height)
    bg_color = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][0])
    ctx.set_source_rgb(bg_color['r'], bg_color['g'], bg_color['b'])
    ctx.fill()

    # circle on circumference
    for x_cnt in range(horizontal_unit_cnt):
        x_start = unit_length * x_cnt

        for y_cnt in range(vartical_unit_cnt):
            y_start = unit_length * y_cnt

            x_center = x_start + (unit_length / 2)
            y_center = y_start + (unit_length / 2)

            draw_circle(ctx, x_center, y_center)

    surface.write_to_png(_img_setting.get_img_file_path())


def draw_circle(ctx, xc, yc):
    """
    Drawing the circle

    Args:
        ctx (cairo.Context): The target context
        xc (float): The x coordinate of the circle center
        yc (float): The y coordinate of the circle center
    """
    param_each = _img_setting.get_param_each()
    margin = param_each['margin']
    circle_radius = param_each['circle_radius']
    unit_radius = (param_each['unit_length'] / 2) - margin - circle_radius

    rotation_angle = math.radians(param_each['rotation_angle'])
    circle_total_cnt = param_each['circle_cnt']
    color = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][1])

    for circle_cnt in range(circle_total_cnt):
        theta = ((2 * math.pi * circle_cnt) /
                 circle_total_cnt) + rotation_angle
        x = xc + (unit_radius * math.cos(theta))
        y = yc - (unit_radius * math.sin(theta))

        ctx.arc(x, y, circle_radius, 0, 2 * math.pi)
        ctx.set_source_rgb(color['r'], color['g'], color['b'])
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
                    'horizontal_unit_cnt',
                    'vartical_unit_cnt',
                    'unit_length',
                    'margin',
                    'circle_radius',
                    'circle_cnt',
                    'rotation_angle',
                    'color_list',
                ],
                'properties': {
                    'horizontal_unit_cnt': {
                        'type': 'integer'
                    },
                    'vartical_unit_cnt': {
                        'type': 'integer'
                    },
                    'unit_length': {
                        'type': 'integer'
                    },
                    'margin': {
                        'type': 'integer'
                    },
                    'circle_radius': {
                        'type': 'integer'
                    },
                    'circle_cnt': {
                        'type': 'integer'
                    },
                    'rotation_angle': {
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
