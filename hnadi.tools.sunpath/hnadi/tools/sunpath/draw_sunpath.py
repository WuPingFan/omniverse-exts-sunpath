__all__ = ["DrawSunpath"]

import math
from omni.ui import scene as sc
from omni.ui import color as cl
import omni.ui as ui
from .sunpath_data import SunpathData


class DrawSunpath:
    def __init__(self, origin, scale, pathmodel: SunpathData):
        self.pathmodel = pathmodel
        self.origin = origin
        self.scale = scale * 10000
        self.draw_anydate_path(pathmodel, pathmodel.datevalue, cl.documentation_nvidia, 1.5)
        self.draw_paths()
        self.draw_compass()

    def sort_points(self, points):
        x_points = list(filter(lambda p: p[0] < 0, points))
        y_min = min(x_points, key=lambda p: p[1])
        id = points.index(y_min) + 1
        return points[id:] + points[:id]

    def points_modify(self, points):
        s_points = []
        for pt in points:
            x = pt[0] * self.scale + self.origin[0]
            y = pt[1] * self.scale + self.origin[1]
            z = pt[2] * self.scale + self.origin[2]
            newpt = [x, y, z]
            s_points.append(newpt)
        return s_points

    def generate_circle_pts(self, offset, step):
        points = []
        sep = 2 * math.pi / 360
        for angle in range(0, 361, step):
            x = self.origin[0] + self.scale * math.cos(sep * angle) * offset
            z = self.origin[2] + self.scale * math.sin(sep * angle) * offset
            points.append([round(x, 3), 0, round(z, 3)])
        return points

    def draw_circle(self, offset, step, color, thickness):
        points = self.generate_circle_pts(offset, step)
        sc.Curve(points, thicknesses=[thickness], colors=[color], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_inner_circles(self):
        for i in range(1, 10, 3):
            s = i * 0.1
            self.draw_circle(s, 15, cl.grey, 1.0)

    def draw_drections(self):
        points = self.generate_circle_pts(1, 45)
        for pt in points:
            sc.Curve([pt, self.origin], thicknesses=[1.0], colors=[cl.gray], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_drection_mark(self):
        points_i = self.generate_circle_pts(1, 45)
        points_o = self.generate_circle_pts(1.06, 45)
        points_t = self.generate_circle_pts(1.15, 45)
        for p1, p2 in zip(points_i, points_o):
            sc.Curve([p1, p2], thicknesses=[1.8], colors=[cl.white], curve_type=sc.Curve.CurveType.LINEAR)
        text = ["E", "ES", "S", "SW", "W", "NW", "N", "EN"]
        for i in range(8):
            x, y, z = points_t[i]
            with sc.Transform(transform=sc.Matrix44.get_translation_matrix(x, y, z)):
                sc.Label(text[i], alignment=ui.Alignment.CENTER, color=cl.documentation_nvidia, size=20)

    def draw_anydate_path(self, pathmodel: SunpathData, datevalue: int, color, thickness):
        points = pathmodel.all_day_position(datevalue)
        sort_pts = self.sort_points(points)
        scale_pts = self.points_modify(sort_pts)
        sc.Curve(scale_pts, thicknesses=[thickness], colors=[color], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_sametime_position(self, pathmodel: SunpathData, hour, color, thickness):
        points = pathmodel.all_year_sametime_position(hour)
        s_points = self.points_modify(points)
        if len(s_points) > 0:
            sc.Curve(s_points, thicknesses=[thickness], colors=[color], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_multi_sametime_position(self, pathmodel: SunpathData, color, thickness):
        for h in range(0, 24, 1):
            self.draw_sametime_position(pathmodel, h, color, thickness)

    def draw_paths(self):
        self.draw_anydate_path(self.pathmodel, 172, cl.white, 1.3)
        self.draw_anydate_path(self.pathmodel, 355, cl.white, 1.3)
        self.draw_anydate_path(self.pathmodel, 80, cl.white, 1.3)
        self.draw_anydate_path(self.pathmodel, 110, cl.grey, 1.0)
        self.draw_anydate_path(self.pathmodel, 295, cl.grey, 1.0)
        self.draw_multi_sametime_position(self.pathmodel, cl.white, 0.5)

    def draw_compass(self):
        self.draw_circle(1, 1, cl.white, 1.1)
        self.draw_circle(1.02, 1, cl.white, 1.1)
        self.draw_circle(1.06, 1, cl.white, 1.1)
        self.draw_inner_circles()
        self.draw_drections()
        self.draw_drection_mark()
