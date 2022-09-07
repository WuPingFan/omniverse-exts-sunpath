__all__ = ["ViewportScene"]

from omni.ui import scene as sc
import omni.ui as ui
from .sunpath_data import SunpathData
from .draw_sunpath import DrawSunpath
from .draw_sphere import draw_movable_sphere
from .gesture import MoveGesture

from . import gol


class ViewportScene:
    def __init__(self, viewport_window: ui.Window, ext_id: str, pathmodel: SunpathData) -> None:
        self._scene_view = None
        self._viewport_window = viewport_window

        with self._viewport_window.get_frame(ext_id):
            self._scene_view = sc.SceneView()
            with self._scene_view.scene:
                transform = sc.Transform()
                move_ges = MoveGesture(transform)
                with transform:
                    DrawSunpath(pathmodel, move_ges)
                    if gol.get_value("sun_state"):
                        draw_movable_sphere()
            self._viewport_window.viewport_api.add_scene_view(self._scene_view)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self._scene_view:
            self._scene_view.scene.clear()
            if self._viewport_window:
                self._viewport_window.viewport_api.remove_scene_view(self._scene_view)
        self._viewport_window = None
        self._scene_view = None
