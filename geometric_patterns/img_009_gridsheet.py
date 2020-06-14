# -*- coding: utf-8 -*-
"""Generate 009 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    width = (param_each['unit_cnt_x'] *
             param_each['unit_length']) + param_each['line_width']
    height = (param_each['unit_cnt_y'] *
              param_each['unit_length']) + param_each['line_width']

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # background color
    ctx.rectangle(0, 0, width, height)
    bg_color = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][0])
    ctx.set_source_rgb(bg_color['r'], bg_color['g'], bg_color['b'])
    ctx.fill()

    # grid
    line_color = clr_cnv.rgb_dict_255_to_1(param_each['color_list'][1])
    line_half_width = param_each['line_width'] / 2
    ctx.set_source_rgb(line_color['r'], line_color['g'], line_color['b'])
    for x_ind in range(0, param_each['unit_cnt_x'] + 1):
        ctx.set_line_width(param_each['line_width'])
        x = (x_ind * param_each['unit_length']) + line_half_width
        ctx.move_to(x, 0)
        ctx.line_to(x, height)
        ctx.stroke()

        for thin_x_ind in range(1, param_each['scale_cnt_per_unit']):
            ctx.set_line_width(
                param_each['line_width'] * param_each['thin_line_ratio'])
            thin_x = x + \
                (thin_x_ind * (param_each['unit_length'] /
                               param_each['scale_cnt_per_unit']))
            ctx.move_to(thin_x, 0)
            ctx.line_to(thin_x, height)
            ctx.stroke()

    for y_ind in range(0, param_each['unit_cnt_y'] + 1):
        ctx.set_line_width(param_each['line_width'])
        y = (y_ind * param_each['unit_length']) + line_half_width
        ctx.move_to(0, y)
        ctx.line_to(width, y)
        ctx.stroke()

        for thin_y_ind in range(1, param_each['scale_cnt_per_unit']):
            ctx.set_line_width(
                param_each['line_width'] * param_each['thin_line_ratio'])
            thin_y = y + \
                (thin_y_ind * (param_each['unit_length'] /
                               param_each['scale_cnt_per_unit']))
            ctx.move_to(0, thin_y)
            ctx.line_to(width, thin_y)
            ctx.stroke()

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
                    'thin_line_ratio',
                    'line_width',
                    'unit_cnt_x',
                    'unit_cnt_y',
                    'scale_cnt_per_unit',
                    'unit_length',
                    'color_list',
                ],
                'properties': {
                    'thin_line_ratio': {
                        'type': 'number',
                        'exclusiveMinimum': 0,
                        'exclusiveMaximum': 1
                    },
                    'line_width': {
                        'type': 'integer'
                    },
                    'unit_cnt_x': {
                        'type': 'integer'
                    },
                    'unit_cnt_y': {
                        'type': 'integer'
                    },
                    'scale_cnt_per_unit': {
                        'type': 'integer'
                    },
                    'unit_length': {
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
