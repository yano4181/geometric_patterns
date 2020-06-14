# -*- coding: utf-8 -*-
"""Generate 008 images."""
from common.setting import ImgSetting
import cairo
import common.color_cnv as clr_cnv
import math


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()
    height = param_each['height']
    width = param_each['width']
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    center_list = get_center_list()
    for center in center_list:
        draw_hexagon(ctx, center[0], center[1], center[2])

    surface.write_to_png(_img_setting.get_img_file_path())


def get_center_list():
    """Get the list of center(x y coordinates and color)."""
    param_each = _img_setting.get_param_each()
    r = param_each['radius']
    x_interval = r + (r * math.sin(math.radians(30)))
    y_interval = 2 * (r * math.cos(math.radians(30)))
    y_init_even = r * math.cos(math.radians(30))
    y_init_odd = 0

    x_total_cnt = param_each['width'] // round(x_interval) + 1
    y_total_cnt = param_each['height'] // round(y_interval) + 2

    color1 = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][0])
    color2 = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][1])
    color3 = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][2])

    center_list = []
    for x_cnt in range(0, x_total_cnt):
        for y_cnt in range(0, y_total_cnt):
            if x_cnt % 2 == 0:
                x = x_cnt * x_interval
                y = y_init_odd + (y_cnt * y_interval)
                if y_cnt % 3 == 0:
                    color = color1
                elif y_cnt % 3 == 1:
                    color = color2
                else:
                    color = color3
            else:
                x = x_cnt * x_interval
                y = y_init_even + (y_cnt * y_interval)
                if y_cnt % 3 == 0:
                    color = color3
                elif y_cnt % 3 == 1:
                    color = color1
                else:
                    color = color2

            center = (x, y, color)
            center_list.append(center)

    return center_list


def draw_hexagon(ctx, xc, yc, color):
    """
    Draw the hexagon

    Args:
        ctx (cairo.Context): The target context
        xc (float): The x coordinate of the hexagon center
        yc (float): The y coordinate of the hexagon center
        color (dict): The color of the hexagon
    """
    param_each = _img_setting.get_param_each()
    r = param_each['radius']
    n = 6

    for m in range(0, n):
        theta = (2 * math.pi * m) / n
        x = xc + (r * math.cos(theta))
        y = yc - (r * math.sin(theta))

        if m == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

    ctx.close_path()
    ctx.set_source_rgb(color['r'], color['g'], color['b'])
    ctx.fill_preserve()
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
                    'width',
                    'height',
                    'radius',
                    'color_list',
                ],
                'properties': {
                    'width': {
                        'type': 'integer'
                    },
                    'height': {
                        'type': 'integer'
                    },
                    'radius': {
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
                    },
                }
            }
        }
    }
}

_img_setting = ImgSetting(__file__, _input_schema)

for i in range(_img_setting.get_param_each_count()):
    gen_img()
