__all__ = ["SunpathData"]

import omni

# Use this method to import pyephem-sunpath packages
omni.kit.pipapi.install("pyephem-sunpath", None, False, False, None, True, True, None)

from pyephem_sunpath.sunpath import sunpos, sunrise, sunset
from datetime import datetime
import math


class SunpathData:
    def __init__(self, datevalue, hour, min, lon, lat):
        self.datevalue = datevalue
        self.hour = hour
        self.lat = lat
        self.lon = lon
        self.min = min
        self.tz = round(self.lon / 15)

    def set_date(self, value):
        self.datevalue = value

    def set_hour(self, value):
        self.hour = value

    def set_min(self, value):
        self.min = value

    def set_longitude(self, value):
        self.lon = value

    def set_latitude(self, value):
        self.lat = value

    @staticmethod
    def calc_xyz(alt, azm):
        x_val = math.sin((azm - 180) * math.pi / 180)
        y_val = math.cos((azm - 180) * math.pi / 180)
        z_val = math.tan(alt * math.pi / 180)
        length = (x_val**2 + y_val**2 + z_val**2) ** 0.5
        return [-x_val / length, z_val / length, y_val / length]

    def dome_rotate_angle(self):
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(2022, month, day, self.hour, self.min)
        alt, azm = sunpos(thetime, self.lat, self.lon, self.tz, dst=False)
        return -alt, 180 - azm

    def get_sun_position(self, thetime, lat, lon, tz):
        alt, azm = sunpos(thetime, lat, lon, tz, dst=False)
        position = self.calc_xyz(alt, azm)
        return position

    def cur_sun_position(self):
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(2022, month, day, self.hour, self.min)
        return self.get_sun_position(thetime, self.lat, self.lon, self.tz)

    def all_day_position(self, datevalue):
        points = []
        month, day = self.slider_to_datetime(datevalue)
        for t in range(24):
            for m in range(0, 60, 5):
                thetime = datetime(2022, month, day, t, m)
                pos = self.get_sun_position(thetime, self.lat, self.lon, self.tz)
                if pos[1] >= 0:
                    points.append(pos)
        return points

    def all_year_sametime_position(self, hour):
        points = []
        for d in range(1, 366):
            month, day = self.slider_to_datetime(d)
            thetime = datetime(2022, month, day, hour)
            pos = self.get_sun_position(thetime, self.lat, self.lon, self.tz)
            if pos[1] >= 0:
                points.append(pos)
        return points

    def get_cur_time(self):
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(2022, month, day, self.hour, self.min)
        return thetime

    def get_sunrise_time(self):
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(2022, month, day, self.hour, self.min)
        return sunrise(thetime, self.lat, self.lon, self.tz, dst=False).time()

    def get_sunset_time(self):
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(2022, month, day, self.hour, self.min)
        return sunset(thetime, self.lat, self.lon, self.tz, dst=False).time()

    @staticmethod
    def slider_to_datetime(datevalue):
        if datevalue <= 31:
            return [1, datevalue]
        if datevalue > 31 and datevalue <= 59:
            return [2, datevalue - 31]
        if datevalue > 59 and datevalue <= 90:
            return [3, datevalue - 59]
        if datevalue > 90 and datevalue <= 120:
            return [4, datevalue - 90]
        if datevalue > 120 and datevalue <= 151:
            return [5, datevalue - 120]
        if datevalue > 151 and datevalue <= 181:
            return [6, datevalue - 151]
        if datevalue > 181 and datevalue <= 212:
            return [7, datevalue - 181]
        if datevalue > 212 and datevalue <= 243:
            return [8, datevalue - 212]
        if datevalue > 243 and datevalue <= 273:
            return [9, datevalue - 243]
        if datevalue > 273 and datevalue <= 304:
            return [10, datevalue - 273]
        if datevalue > 304 and datevalue <= 334:
            return [11, datevalue - 304]
        if datevalue > 334 and datevalue <= 365:
            return [12, datevalue - 334]
