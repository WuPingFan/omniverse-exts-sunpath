__all__ = ["SunpathData"]


import omni

# Use this method to import pyephem-sunpath packages
omni.kit.pipapi.install("pyephem-sunpath", None, False, False, None, True, True, None)

import math
from datetime import datetime
from pyephem_sunpath.sunpath import sunpos, sunrise, sunset


class SunpathData:
    """Generate sunpath data"""

    def __init__(self, datevalue, hour, min, lon, lat):
        self.datevalue = datevalue
        self.year = datetime.now().year
        self.hour = hour
        self.lat = lat
        self.lon = lon
        self.min = min

        # Compute the timezone
        self.tz = round(self.lon / 15)

    def set_date(self, value):
        """
        The method to reset date parameter
        """
        self.datevalue = value

    def set_hour(self, value):
        """
        The method to reset hour parameter
        """
        self.hour = value

    def set_min(self, value):
        """
        The method to reset minite parameter
        """
        self.min = value

    def set_longitude(self, value):
        """
        The method to reset longitude parameter
        """
        self.lon = value

    def set_latitude(self, value):
        """
        The method to reset latitude parameter
        """
        self.lat = value

    @staticmethod
    def calc_xyz(alt, azm):
        """
        Convert spherical coordinates to Cartesian coordinates
        """
        x_val = math.sin((azm - 180) * math.pi / 180)
        y_val = math.cos((azm - 180) * math.pi / 180)
        z_val = math.tan(alt * math.pi / 180)
        length = (x_val**2 + y_val**2 + z_val**2) ** 0.5
        return [-x_val / length, z_val / length, y_val / length]

    def dome_rotate_angle(self):
        """
        Compute dome rotate angle
        """
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(self.year, month, day, self.hour, self.min)
        alt, azm = sunpos(thetime, self.lat, self.lon, self.tz, dst=False)
        return -alt, 180 - azm

    def get_sun_position(self, thetime, lat, lon, tz):
        """
        Get sun position of exact time
        """
        alt, azm = sunpos(thetime, lat, lon, tz, dst=False)
        position = self.calc_xyz(alt, azm)
        return position

    def cur_sun_position(self):
        """
        Get sun position of  current time(input)
        """
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(self.year, month, day, self.hour, self.min)
        return self.get_sun_position(thetime, self.lat, self.lon, self.tz)

    def all_day_position(self, datevalue):
        """
        Get sun posion of all day(exact date)
        """
        points = []
        month, day = self.slider_to_datetime(datevalue)
        for t in range(24):
            for m in range(0, 60, 5):
                thetime = datetime(self.year, month, day, t, m)
                pos = self.get_sun_position(thetime, self.lat, self.lon, self.tz)
                if pos[1] >= 0:
                    points.append(pos)
        return points

    def all_year_sametime_position(self, hour):
        """
        Get all year sametime position
        """
        points = []
        for d in range(1, 366, 2):
            month, day = self.slider_to_datetime(d)
            thetime = datetime(self.year, month, day, hour)
            pos = self.get_sun_position(thetime, self.lat, self.lon, self.tz)
            if pos[1] >= 0:
                points.append(pos)
        if len(points) > 0:
            points.append(points[0])
        return points

    def get_cur_time(self):
        """
        Get current datetime(input)
        """
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(self.year, month, day, self.hour, self.min)
        return thetime

    def get_sunrise_time(self):
        """
        Get sunrise time of exact date
        """
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(self.year, month, day, self.hour, self.min)
        return sunrise(thetime, self.lat, self.lon, self.tz, dst=False).time()

    def get_sunset_time(self):
        """
        Get sunset time of exact date
        """
        month, day = self.slider_to_datetime(self.datevalue)
        thetime = datetime(self.year, month, day, self.hour, self.min)
        return sunset(thetime, self.lat, self.lon, self.tz, dst=False).time()

    @staticmethod
    def slider_to_datetime(datevalue):
        """
        Convert slider value to datetime
        """
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
