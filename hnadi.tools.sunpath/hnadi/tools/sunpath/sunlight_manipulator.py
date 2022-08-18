__all__ = ["SunlightManipulator"]

import omni.kit.commands
from pxr import Gf, Sdf
from .sunpath_data import SunpathData


class SunlightManipulator:
    def __init__(self, pathmodel: SunpathData, scale: float):
        self.path = None
        self.scale = scale * 10000
        self.sun_model = pathmodel

    def add_sun(self):
        omni.kit.commands.execute("CreatePrim", prim_type="DistantLight", attributes={"angle": 1.0, "intensity": 3000})
        self.path = "/World/DistantLight"

    def move_sun(self, position, scale):
        x = position[0] * scale
        y = position[1] * scale
        z = position[2] * scale
        xr, yr = self.sun_model.dome_rotate_angle()
        if y < 0:
            omni.kit.commands.execute(
                "ChangeProperty", prop_path=Sdf.Path("/World/DistantLight.visibility"), value="invisible", prev=None
            )
        else:
            omni.kit.commands.execute(
                "ChangeProperty", prop_path=Sdf.Path("/World/DistantLight.visibility"), value="inherited", prev=None
            )
        omni.kit.commands.execute(
            "TransformPrimSRT",
            path=Sdf.Path("/World/DistantLight"),
            new_translation=Gf.Vec3d(x, y, z),
            new_rotation_euler=Gf.Vec3d(xr, yr, 0),
        )

    def show_sun(self):
        if self.path is None:
            self.add_sun()
        self.move_sun(self.sun_model.cur_sun_position(), self.scale)

    def del_sun(self):
        if self.path is not None:
            omni.kit.commands.execute("DeletePrims", paths=["/World/DistantLight"])
            self.path = None
