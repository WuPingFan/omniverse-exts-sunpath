import math
from math import sin, cos
import numpy as np
from omni.ui import scene as sc
from omni.ui import color as cl

from . import gol


def rotate_matrix_z(angle):
    """
    Build Z-axis rotation matrix
    """
    sep = 2 * math.pi / 360
    Rz = [
        [cos(sep * angle), -sin(sep * angle), 0],
        [sin(sep * angle), cos(sep * angle), 0],
        [0, 0, 1],
    ]
    return np.array(Rz)


def rotate_points(points, angle):
    """
    rotate a point list
    """
    rotated_pts = []
    for pt in points:
        pt_arr = np.array(pt)
        Rz = rotate_matrix_z(angle)
        rotated_pt = list(np.dot(Rz, pt_arr))
        rotated_pts.append(rotated_pt)
    return rotated_pts


def generate_circle_pts(offset, step, scale):
    """
    Generate the points that make up the circle
    """
    points = []
    sep = 2 * math.pi / 360
    for angle in range(0, 361, step):
        x = scale * math.cos(sep * angle) * offset
        z = scale * math.sin(sep * angle) * offset
        points.append([round(x, 3), 0, round(z, 3)])
    return points


def draw_base_sphere():
    """
    Draw a shpere base on [0,0,0]
    """
    scale = gol.get_value("scale") * 200
    points = generate_circle_pts(0.1, 5, scale)

    sc.Curve(points, thicknesses=[1], colors=[cl.beige], curve_type=sc.Curve.CurveType.LINEAR)

    for angle in range(0, 361, 4):
        r_pts = rotate_points(points, angle)
        sc.Curve(r_pts, thicknesses=[1], colors=[cl.beige], curve_type=sc.Curve.CurveType.LINEAR)


def points_modify(points):
    """
    Change the coordinates of the point based on the origin and scale
    """
    scale = gol.get_value("scale") * 200
    origin = gol.get_value("origin")

    s_points = []
    for pt in points:
        x = pt[0] * scale + origin[0]
        y = pt[1] * scale + origin[1]
        z = pt[2] * scale + origin[2]
        newpt = [x, y, z]
        s_points.append(newpt)
    return s_points


def draw_movable_sphere():
    """
    According parametes to move sphere positon
    """
    pathmodel = gol.get_value("pathmodel")
    sun_pos = pathmodel.cur_sun_position()
    x, y, z = points_modify([sun_pos])[0]
    if y > 0:
        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(x, y, z)):
            draw_base_sphere()
