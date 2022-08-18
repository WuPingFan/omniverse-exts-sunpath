__all__ = ["ViewportScene"]

from .sunpath_data import SunpathData
from omni.ui import scene as sc
import omni.ui as ui
from .draw_sunpath import DrawSunpath


class ViewportScene:
    def __init__(self, viewport_window: ui.Window, ext_id: str, scale: int, pathmodel: SunpathData) -> None:
        self._scene_view = None
        self._viewport_window = viewport_window
        self.scale = scale

        with self._viewport_window.get_frame(ext_id):
            self._scene_view = sc.SceneView()
            with self._scene_view.scene:
                DrawSunpath([0, 0, 0], self.scale, pathmodel)
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
