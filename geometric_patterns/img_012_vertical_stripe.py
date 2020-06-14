# -*- coding: utf-8 -*-
"""Generate 012 images."""
import cairo
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    width = param_each['width']
    height = param_each['height']

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # background color
    ctx.rectangle(0, 0, width, height)
    bg_color = clr_cnv.rgb_dict_255_to_1(param_each['background_color'])
    ctx.set_source_rgb(bg_color['r'], bg_color['g'], bg_color['b'])
    ctx.fill()

    # stripe
    stripe_list = param_each['stripe_list']
    stripe_x_coordinate = 0
    stripe_ind = 0
    while stripe_x_coordinate < width:
        stripe = stripe_list[stripe_ind]
        stripe_left_margin = stripe['left_margin']
        stripe_width = stripe['width']
        stripe_color = clr_cnv.rgb_dict_255_to_1(stripe['color'])
        stripe_x_coordinate += stripe_left_margin
        ctx.set_source_rgb(stripe_color['r'],
                           stripe_color['g'], stripe_color['b'])

        ctx.set_line_width(stripe_width)
        ctx.move_to(stripe_x_coordinate, 0)
        ctx.line_to(stripe_x_coordinate, height)
        ctx.stroke()

        stripe_x_coordinate += stripe_width

        stripe_ind = stripe_ind + 1 if stripe_ind + 1 < len(stripe_list) else 0

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
                    'width',
                    'height',
                    'background_color',
                    'stripe_list',
                ],
                'properties': {
                    'width': {
                        'type': 'integer'
                    },
                    'height': {
                        'type': 'integer'
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
                    'stripe_list': {
                        'type': 'array',
                        'minItems': 1,
                        'items': {
                            'type': 'object',
                            'required': ['left_margin', 'width', 'color'],
                            'properties': {
                                'left_margin': {
                                    'type': 'integer'
                                },
                                'width': {
                                    'type': 'integer'
                                },
                                'color': {
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
                                    },
                                }
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
