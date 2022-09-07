__all__ = ["DrawSunpath"]

import math
from omni.ui import scene as sc
from omni.ui import color as cl
import omni.ui as ui
from .sunpath_data import SunpathData

from . import gol


class DrawSunpath:
    def __init__(self, pathmodel: SunpathData, move_ges):
        self.move_ges = move_ges
        self.pathmodel = pathmodel
        self.origin = gol.get_value("origin")
        self.scale = gol.get_value("scale") * 200
        self.color = cl(*gol.get_value("color"))
        # Draw sunpath
        self.draw_anydate_path(self.pathmodel, self.pathmodel.datevalue, cl.documentation_nvidia, 1.5)
        self.draw_paths()
        self.draw_compass()
        if gol.get_value("show_info"):
            self.show_info()

    def sort_points(self, points):
        """
        Resort the points to make sure they connect to a reasonable curve
        """
        x_points = list(filter(lambda p: p[0] < 0, points))
        if len(x_points) != 0:
            y_min = min(x_points, key=lambda p: p[1])
            id = points.index(y_min) + 1
            return points[id:] + points[:id]
        return points

    def points_modify(self, points):
        """
        Change the coordinates of the point based on the origin
        """
        s_points = []
        for pt in points:
            x = pt[0] * self.scale + self.origin[0]
            y = pt[1] * self.scale + self.origin[1]
            z = pt[2] * self.scale + self.origin[2]
            newpt = [x, y, z]
            s_points.append(newpt)
        return s_points

    def generate_circle_pts(self, offset, step):
        """
        Generate the points that make up the circle or present anchor point
        """
        points = []
        sep = 2 * math.pi / 360
        for angle in range(0, 361, step):
            x = self.origin[0] + self.scale * math.cos(sep * angle) * offset
            z = self.origin[2] + self.scale * math.sin(sep * angle) * offset
            points.append([round(x, 3), 0, round(z, 3)])
        return points

    def draw_circle(self, offset, step, color, thickness):
        """
        Connet points to draw a circle
        """
        points = self.generate_circle_pts(offset, step)
        sc.Curve(points, thicknesses=[thickness], colors=[color], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_drections(self):
        """
        Draw cross line and mark main directions
        """
        # Generate anchor point
        points_a = self.generate_circle_pts(1.15, 90)
        points_b = self.generate_circle_pts(1.25, 90)
        points_c = self.generate_circle_pts(1.15, 2)
        points_t = self.generate_circle_pts(1.33, 90)

        for pt in points_b:
            sc.Curve([pt, self.origin], thicknesses=[1.0], colors=[cl.gray], curve_type=sc.Curve.CurveType.LINEAR)
        arrow = []
        for i in range(1, 181, 45):
            arrow.append(points_c[i])
        # Draw arrow
        for p_a, p_b, p_c in zip(points_a, points_b, arrow):
            sc.Curve(
                [p_b, p_c, p_a, p_b],
                thicknesses=[1.5],
                colors=[cl.documentation_nvidia],
                curve_type=sc.Curve.CurveType.LINEAR,
            )
        # Draw diretions label
        text = ["E", "S", "W", "N"]
        for i in range(4):
            x, y, z = points_t[i]
            with sc.Transform(transform=sc.Matrix44.get_translation_matrix(x, y, z)):
                sc.Label(text[i], alignment=ui.Alignment.CENTER, color=cl.documentation_nvidia, size=20)

    def draw_drection_mark(self):
        """
        Draw degrees directions and add a move gesture
        """
        points_a = self.generate_circle_pts(1, 30)
        points_b = self.generate_circle_pts(1.06, 30)
        points_g = self.generate_circle_pts(1.03, 90)
        points_t = self.generate_circle_pts(1.1, 30)

        # Compute length of tick-mark line
        length = points_b[3][2] - points_a[3][2]
        gol.set_value("length", length)

        # Add move gesture block
        x, y, z = points_g[3]
        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(x, y, z)):
            sc.Rectangle(
                axis=ui.Axis.X,
                color=cl.documentation_nvidia,
                width=length / 2,
                height=length,
                gesture=self.move_ges,
            )

        # Add tick-mark line
        for p1, p2 in zip(points_a, points_b):
            sc.Curve(
                [p1, p2], thicknesses=[1.5], colors=[cl.documentation_nvidia], curve_type=sc.Curve.CurveType.LINEAR
            )

        # Add degree label
        text = [f"{d}" for d in list(range(0, 361, 30))]
        text = text[3:12] + text[:3]
        for i in range(12):
            x, y, z = points_t[i]
            with sc.Transform(transform=sc.Matrix44.get_translation_matrix(x, y, z)):
                sc.Label(text[i], alignment=ui.Alignment.CENTER, color=cl.documentation_nvidia, size=12)

    def draw_anydate_path(self, pathmodel: SunpathData, datevalue: int, color, thickness):
        """
        The method to draw the path of sun on exact date
        """
        points = pathmodel.all_day_position(datevalue)
        sort_pts = self.sort_points(points)
        scale_pts = self.points_modify(sort_pts)
        if len(scale_pts) > 0:
            sc.Curve(scale_pts, thicknesses=[thickness], colors=[color], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_sametime_position(self, pathmodel: SunpathData, hour, color, thickness):
        """
        The method to draw the path of sun on diffrent date but in same time,'8' shape curve
        """
        points = pathmodel.all_year_sametime_position(hour)
        sort_pts = self.sort_points(points)
        scale_pts = self.points_modify(sort_pts)
        if len(scale_pts) > 0:
            sc.Curve(scale_pts, thicknesses=[thickness], colors=[color], curve_type=sc.Curve.CurveType.LINEAR)

    def draw_multi_sametime_position(self, pathmodel: SunpathData, color, thickness):
        """
        Draw twenty four '8' shape curves
        """
        for h in range(0, 24, 1):
            self.draw_sametime_position(pathmodel, h, color, thickness)

    def draw_paths(self):
        """
        Draw diffrent path
        """
        self.draw_anydate_path(self.pathmodel, 172, self.color, 1.3)
        self.draw_anydate_path(self.pathmodel, 355, self.color, 1.3)
        self.draw_anydate_path(self.pathmodel, 80, self.color, 1.3)
        self.draw_anydate_path(self.pathmodel, 110, cl.grey, 1.0)
        self.draw_anydate_path(self.pathmodel, 295, cl.grey, 1.0)
        self.draw_multi_sametime_position(self.pathmodel, self.color, 0.5)

    def draw_compass(self):
        """
        Draw entire compass
        """
        self.draw_circle(1, 1, self.color, 1.1)
        self.draw_circle(1.04, 1, self.color, 1.1)
        self.draw_drections()
        self.draw_drection_mark()

    def show_info(self):
        """
        Draw information label
        """
        anchor = self.generate_circle_pts(1.5, 90)
        anchor_e = anchor[0]
        anchor_w = anchor[2]
        anchor_n = anchor[3]
        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*anchor_e)):
            sc.Label(
                f"sunrise: {self.pathmodel.get_sunrise_time()}".upper(),
                alignment=ui.Alignment.RIGHT_CENTER,
                color=cl.beige,
                size=16,
            )
        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*anchor_w)):
            sc.Label(
                f"sunset: {self.pathmodel.get_sunset_time()}".upper(),
                alignment=ui.Alignment.LEFT_CENTER,
                color=cl.beige,
                size=16,
            )
        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*anchor_n)):
            sc.Label(
                f"datetime: {self.pathmodel.get_cur_time()}".upper(),
                alignment=ui.Alignment.LEFT_CENTER,
                color=cl.beige,
                size=16,
            )
