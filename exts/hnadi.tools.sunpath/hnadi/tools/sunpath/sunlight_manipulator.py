__all__ = ["SunlightManipulator"]

from .sunpath_data import SunpathData
from pxr import Gf, Sdf
import omni.kit.commands

from . import gol


class SunlightManipulator:
    def __init__(self, pathmodel: SunpathData):
        self.path = None

        # Get origin value from global dictionary
        self.origin = gol.get_value("origin")
        self.pathmodel = pathmodel

    def add_sun(self):
        """
        Add distant light to present sunlight
        """
        omni.kit.commands.execute("CreatePrim", prim_type="DistantLight", attributes={"angle": 1.0, "intensity": 3000})
        self.path = "/World/DistantLight"

    def change_sun(self):
        """
        Change distant light property(rotation)
        """

        xr, yr = self.pathmodel.dome_rotate_angle()
        if [xr, yr] != gol.get_value("dome_angle"):
            omni.kit.commands.execute(
                "TransformPrimSRT",
                path=Sdf.Path("/World/DistantLight"),
                new_rotation_euler=Gf.Vec3d(xr, yr, 0),
            )
            x, y, z = self.pathmodel.cur_sun_position()
            if y < 0:
                omni.kit.commands.execute(
                    "ChangeProperty", prop_path=Sdf.Path("/World/DistantLight.visibility"), value="invisible", prev=None
                )
            else:
                omni.kit.commands.execute(
                    "ChangeProperty", prop_path=Sdf.Path("/World/DistantLight.visibility"), value="inherited", prev=None
                )
        gol.set_value("dome_angle", [xr, yr])

    def show_sun(self):
        """
        The method to add light and change it's property
        """
        if self.path is None:
            self.add_sun()
        self.change_sun()

    def del_sun(self):
        """
        the method to delete exisit distant light
        """
        if self.path is not None:
            omni.kit.commands.execute("DeletePrims", paths=["/World/DistantLight"])
            self.path = None
