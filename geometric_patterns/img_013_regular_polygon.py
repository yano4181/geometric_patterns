# -*- coding: utf-8 -*-
"""Generate 013 images."""
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

    # regular poygons
    for x_cnt in range(horizontal_unit_cnt):
        x_start = unit_length * x_cnt

        for y_cnt in range(vartical_unit_cnt):
            y_start = unit_length * y_cnt

            x_center = x_start + (unit_length / 2)
            y_center = y_start + (unit_length / 2)

            draw_polygon(ctx, x_center, y_center)

    surface.write_to_png(_img_setting.get_img_file_path())


def draw_polygon(ctx, xc, yc):
    """
    Drawing the polygon

    Args:
        ctx (cairo.Context): The target context
        xc (float): The x coordinate of the hexagon center
        yc (float): The y coordinate of the hexagon center
    """
    param_each = _img_setting.get_param_each()
    line_width = param_each['line_width']
    radius = (param_each['unit_length'] / 2) - line_width
    edge_total_cnt = param_each['edge_cnt']
    rotation_angle = math.radians(param_each['rotation_angle'])
    color = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][1])

    for edge_cnt in range(0, edge_total_cnt):
        theta = ((2 * math.pi * edge_cnt) / edge_total_cnt) + rotation_angle
        x = xc + (radius * math.cos(theta))
        y = yc - (radius * math.sin(theta))

        if edge_cnt == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

    ctx.close_path()
    ctx.set_source_rgb(color['r'], color['g'], color['b'])
    ctx.set_line_width(line_width)

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
                    'edge_cnt',
                    'rotation_angle',
                    'horizontal_unit_cnt',
                    'vartical_unit_cnt',
                    'unit_length',
                    'line_width',
                    'color_list',
                ],
                'properties': {
                    'edge_cnt': {
                        'type': 'integer'
                    },
                    'rotation_angle': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': 360
                    },
                    'horizontal_unit_cnt': {
                        'type': 'integer'
                    },
                    'vartical_unit_cnt': {
                        'type': 'integer'
                    },
                    'unit_length': {
                        'type': 'integer'
                    },
                    'line_width': {
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
