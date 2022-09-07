from omni.ui import scene as sc
from omni.ui import color as cl

from . import gol


class _ViewportLegacyDisableSelection:
    """Disables selection in the Viewport Legacy"""

    def __init__(self):
        self._focused_windows = None
        focused_windows = []
        try:
            import omni.kit.viewport_legacy as vp

            vpi = vp.acquire_viewport_interface()
            for instance in vpi.get_instance_list():
                window = vpi.get_viewport_window(instance)
                if not window:
                    continue
                focused_windows.append(window)
            if focused_windows:
                self._focused_windows = focused_windows
                for window in self._focused_windows:
                    window.disable_selection_rect(True)
        except Exception:
            pass


class MoveGesture(sc.DragGesture):
    """Define the action of gesture"""

    def __init__(self, transform: sc.Transform):
        super().__init__()
        self.__transform = transform
        self._previous_ray_point = None
        self._pre_origin = None

    def on_began(self):
        self.sender.color = cl.beige
        self.sender.width = gol.get_value("length")
        self.disable_selection = _ViewportLegacyDisableSelection()
        self._previous_ray_point = self.gesture_payload.ray_closest_point
        self._pre_origin = gol.get_value("origin")

    def on_changed(self):
        translate = self.sender.gesture_payload.moved
        current = sc.Matrix44.get_translation_matrix(*translate)
        self.__transform.transform *= current

        object_ray_point = self.gesture_payload.ray_closest_point

        # Compute translation vector(point)
        moved = [a - b for a, b in zip(object_ray_point, self._previous_ray_point)]

        # Compute new origin and save it to dictionary
        origin = [a + b for a, b in zip(self._pre_origin, moved)]
        gol.set_value("origin", origin)

    def on_ended(self):
        self.sender.color = cl.documentation_nvidia
        self.sender.width = gol.get_value("length") / 2
        self.disable_selection = None
