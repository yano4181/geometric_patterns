# -*- coding: utf-8 -*-
"""Generate 016 images."""
import cairo
import math
import random
from common.setting import ImgSetting
import common.color_cnv as clr_cnv


def gen_img():
    """Generate the image."""
    param_each = _img_setting.get_param_each()

    width = param_each['width']
    height = param_each['height']

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(surface)

    # color list
    color_list = list(map(clr_cnv.rgb_dict_255_to_1, param_each['color_list']))

    # background color
    ctx.rectangle(0, 0, width, height)
    bg_color = color_list[0]
    ctx.set_source_rgb(bg_color['r'], bg_color['g'], bg_color['b'])
    ctx.fill()

    # star size
    star_full_size = get_star_full_size()

    # coordinates of star center
    star_center_list = get_star_center_list(star_full_size)

    # draw stars
    for star_center in star_center_list:
        star_color = color_list[random.randint(1, len(color_list) - 1)]

        pentagon_vertex_list = get_pentagon_vertex_list(
            star_center['x'], star_center['y'])

        # star variation
        # 0: fill, 1: outer frame, 2 one stroke
        star_variation = random.randint(0, 2)
        star_vertex_list = get_star_vertex_list(pentagon_vertex_list)

        if star_variation == 0:
            draw_fill_polygon(ctx, star_vertex_list, star_color)
        elif star_variation == 1:
            draw_line_polygon(ctx, star_vertex_list, star_color)
        elif star_variation == 2:
            pentagram_vertex_list = get_pentagram_vertex_list(
                pentagon_vertex_list)
            draw_line_polygon(ctx, pentagram_vertex_list, star_color)

    surface.write_to_png(_img_setting.get_img_file_path())


def get_star_full_size():
    """
    Get the size of star with margin.

    Returns:
        float: The size of star with margin
    """
    param_each = _img_setting.get_param_each()
    width = param_each['width']
    height = param_each['height']
    hrz_num = param_each['horizontal_star_num']
    vrt_num = param_each['vertical_star_num']

    hrz_size = width / hrz_num
    vrt_size = height / vrt_num

    full_size = hrz_size if hrz_size < vrt_size else vrt_size

    return full_size


def get_star_radius():
    """
    Get the star radius.

    Returns:
        float: The star radius
    """
    return (get_star_full_size() / 2) * (9 / 10)


def get_star_center_list(star_full_size):
    """
    Get the star center coordinates list.

    Args:
        star_full_size (float): The star size with margin

    Returns:
        list: The star center coordinate list
    """
    param_each = _img_setting.get_param_each()

    star_center_list = list()
    width = param_each['width']
    height = param_each['height']

    # horizontal
    hrz_num = param_each['horizontal_star_num']
    hrz_size = width / hrz_num
    hrz_top_y = star_full_size / 2
    hrz_btm_y = height - (star_full_size / 2)
    for ind in range(hrz_num):
        x = (hrz_size * ind) + (hrz_size / 2)
        star_center_list.append({'x': x, 'y': hrz_top_y})
        star_center_list.append({'x': x, 'y': hrz_btm_y})

    # vertical (trim the first and last stars)
    vrt_num = param_each['vertical_star_num']
    vrt_size = height / vrt_num
    vrt_left_x = star_full_size / 2
    vrt_right_x = width - (star_full_size / 2)
    for ind in range(1, vrt_num - 1):
        y = (vrt_size * ind) + (vrt_size / 2)
        star_center_list.append({'x': vrt_left_x, 'y': y})
        star_center_list.append({'x': vrt_right_x, 'y': y})

    return star_center_list


def draw_fill_polygon(ctx, star_vertex_list, color):
    """
    Draw the star.

    Args:
        ctx (cairo.Context): The target context
        star_vertex_list (list): The star vertex list
        color (dict): The color of the hexagon
    """

    for vertex_ind, vertex in enumerate(star_vertex_list):
        x = vertex['x']
        y = vertex['y']
        if vertex_ind == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

    ctx.close_path()
    ctx.set_source_rgb(color['r'], color['g'], color['b'])
    ctx.fill_preserve()
    ctx.stroke()


def draw_line_polygon(ctx, star_vertex_list, color):
    """
    Draw the star.

    Args:
        ctx (cairo.Context): The target context
        star_vertex_list (list): The star vertex list
        color (dict): The color of the hexagon
    """

    for vertex_ind, vertex in enumerate(star_vertex_list):
        x = vertex['x']
        y = vertex['y']
        if vertex_ind == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

    ctx.close_path()
    ctx.set_source_rgb(color['r'], color['g'], color['b'])
    ctx.stroke()


def get_pentagon_vertex_list(xc, yc):
    """
    Get the pentagon vertex list.

    Args:
        xc (float): The x coordinate of the pentagon center
        yc (float): The y coordinate of the pentagon center

    Returns:
        list: The pentagon vertex list
    """
    radius = get_star_radius()
    n = 5
    angle_adj = ((1 / 2) - (2 / 5)) * math.pi
    pentagon_vertex_list = list()

    for m in range(0, n):
        theta = ((2 * math.pi * m) / n) + angle_adj
        x = xc + (radius * math.cos(theta))
        y = yc - (radius * math.sin(theta))

        pentagon_vertex_list.append({'x': x, 'y': y})

    return pentagon_vertex_list


def get_star_vertex_list(pentagon_vertex_list):
    """
    Get the star vertex list.

    Args:
        pentagon_vertex_list (list): The pentagon vertex list

    Returns:
        list: The star vertex list
    """
    star_vertex_list = list()
    line_point_diff_ind = 2
    two_lines_diff_ind = 4
    max_ind = 4
    for m in range(len(pentagon_vertex_list)):

        l1_p1_ind = m
        l1_p1 = pentagon_vertex_list[l1_p1_ind]
        l1_p2_ind = adj_num_if_greater_than_n(
            l1_p1_ind + line_point_diff_ind, max_ind)
        l1_p2 = pentagon_vertex_list[l1_p2_ind]

        l2_p1_ind = adj_num_if_greater_than_n(
            l1_p1_ind + two_lines_diff_ind, max_ind)
        l2_p1 = pentagon_vertex_list[l2_p1_ind]
        l2_p2_ind = adj_num_if_greater_than_n(
            l2_p1_ind + line_point_diff_ind, max_ind)
        l2_p2 = pentagon_vertex_list[l2_p2_ind]

        star_vertex_list.append(pentagon_vertex_list[m])
        star_vertex_list.append(get_intersection(l1_p1, l1_p2, l2_p1, l2_p2))

    return star_vertex_list


def get_pentagram_vertex_list(pentagon_vertex_list):
    """
    Get the pentagram vertex list.

    Args:
        pentagon_vertex_list (list): The pentagon vertex list

    Returns:
        list: The pentagram vertex list
    """
    pentagram_vertex_list = list()

    for m in [0, 2, 4, 1, 3]:
        pentagram_vertex_list.append(pentagon_vertex_list[m])

    return pentagram_vertex_list


def adj_num_if_greater_than_n(num, n):
    """
    Adjust the number if the number is greater than n.

    Args:
        num (int): The number
        n (int): n

    Returns:
        int: The adjusted number
    """
    return num - (n + 1) if num > n else num


def get_intersection(l1_p1, l1_p2, l2_p1, l2_p2):
    """
    Get the intersection of 2 lines.

    Args:
        l1_p1 (dict): One point on line1
        l1_p2 (dict): Another point on line1
        l2_p1 (dict): One point on line2
        l2_p2 (dict): Another point on line2

    Returns:
        dict: The intersection of 2 lines
    """
    l1_slope = (l1_p2['y'] - l1_p1['y']) / (l1_p2['x'] - l1_p1['x'])
    l1_intercept = l1_p1['y'] - (l1_slope * l1_p1['x'])
    l2_slope = (l2_p2['y'] - l2_p1['y']) / (l2_p2['x'] - l2_p1['x'])
    l2_intercept = l2_p1['y'] - (l2_slope * l2_p1['x'])

    intersection_x = (l2_intercept - l1_intercept) / (l1_slope - l2_slope)
    intersection_y = ((l1_slope * l2_intercept) -
                      (l2_slope * l1_intercept)) / (l1_slope - l2_slope)

    return {'x': intersection_x, 'y': intersection_y}


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
                    'vertical_star_num',
                    'horizontal_star_num',
                    'color_list',
                ],
                'properties': {
                    'width': {
                        'type': 'integer'
                    },
                    'height': {
                        'type': 'integer'
                    },
                    'vertical_star_num': {
                        'type': 'integer'
                    },
                    'horizontal_star_num': {
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
