__all__ = ["SunpathExtension"]

from .window import SunpathWindow
from functools import partial
import asyncio
import omni.ext
import omni.kit.ui
import omni.ui as ui
from omni.kit.viewport.utility import get_active_viewport_window
from .viewport_scene import ViewportScene
from .sunlight_manipulator import SunlightManipulator

# Import global dictionary
from . import gol

# Initialize dictionary
gol._init()


class SunpathExtension(omni.ext.IExt):

    WINDOW_NAME = "sunpath extension".upper()
    MENU_PATH = f"Window/{WINDOW_NAME}"

    def __init__(self):
        self._window = None
        # Get acive viewport window
        self.viewport_window = get_active_viewport_window()
        self._viewport_scene = None
        # Preset display toggle
        self._show_path = False
        self._show_sun = False
        # Preset path model and sunlight model
        self.pathmodel = gol.get_value("pathmodel")
        self.sunlightmodel = SunlightManipulator(self.pathmodel)

    def on_startup(self, ext_id):
        # Add ext_id key value
        self.ext_id = ext_id

        # The ability to show up the window if the system requires it. We use it
        # in QuickLayout.
        ui.Workspace.set_show_window_fn(SunpathExtension.WINDOW_NAME, partial(self.show_window, None))

        # Put the new menu
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item(SunpathExtension.MENU_PATH, self.show_window, toggle=True, value=True)

        # Show the window. It will call `self.show_window`
        ui.Workspace.show_window(SunpathExtension.WINDOW_NAME)

    def on_shutdown(self):
        """
        Destroy viewport scene and window
        """
        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = None
        self._menu = None
        if self._window:
            self._window.destroy()
            self._window = None

        # Deregister the function that shows the window from omni.ui
        ui.Workspace.set_show_window_fn(SunpathExtension.WINDOW_NAME, None)

    def sunpath_toggle(self, value):
        """
        The method to change the toggle, this dropped into the window
        """
        if value:
            self._show_path = value
            self._viewport_scene = ViewportScene(self.viewport_window, self.ext_id, self.pathmodel)
        else:
            self._show_path = value
            self._viewport_scene.destroy()
            self._viewport_scene = None

    def sunlight_toggle(self, value):
        """
        The method to change the toggle, this dropped into the window file
        """
        if value:
            self._show_sun = value
            self.sunlightmodel.show_sun()
        else:
            self._show_sun = value
            self.sunlightmodel.del_sun()
        gol.set_value("sun_state", value)

    def update_viewport_scene(self):
        """
        The method to upadate viewport scene
        """
        if self._show_sun:
            self.sunlightmodel = SunlightManipulator(self.pathmodel)
            self.sunlightmodel.path = "/World/DistantLight"
            self.sunlightmodel.show_sun()

        if self._show_path:
            if self._viewport_scene is not None:
                self._viewport_scene.destroy()
            self._viewport_scene = ViewportScene(self.viewport_window, self.ext_id, self.pathmodel)

    def update_parameter(self, valtype, val):
        """
        The method to change parameters and update viewport scene, this dropped into window file
        """
        if valtype is None:
            pass
        if valtype == "show_info":
            gol.set_value("show_info", val)
        if valtype == 0:
            gol.set_value("color_r", val * 255)
        if valtype == 1:
            gol.set_value("color_g", val * 255)
        if valtype == 2:
            gol.set_value("color_b", val * 255)
        if valtype == "scale":
            gol.set_value("scale", val)
        if valtype == "longitude":
            self.pathmodel.set_longitude(val)
        if valtype == "latitude":
            self.pathmodel.set_latitude(val)
        if valtype == "date":
            self.pathmodel.set_date(val)
        if valtype == "hour":
            self.pathmodel.set_hour(val)

        # Save pathmodel to dictionary
        gol.set_value("pathmodel", self.pathmodel)

        if valtype == "minite":
            self.pathmodel.set_min(val)
        self.update_viewport_scene()

    def _set_menu(self, value):
        """
        Set the menu to create this window on and off
        """
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(SunpathExtension.MENU_PATH, value)

    async def _destroy_window_async(self):
        # wait one frame, this is due to the one frame defer
        # in Window::_moveToMainOSWindow()
        await omni.kit.app.get_app().next_update_async()
        if self._window:
            self._window.destroy()
            self._window = None

    def _visiblity_changed_fn(self, visible):
        # Called when the user pressed "X"
        self._set_menu(visible)
        if not visible:
            # Destroy the window, since we are creating new window
            # in show_window
            asyncio.ensure_future(self._destroy_window_async())

    def show_window(self, menu, value):
        """
        Show window and deliver some method to it
        """
        if value:
            self._window = SunpathWindow(
                SunpathExtension.WINDOW_NAME,
                delegate_1=self.update_parameter,
                delegate_2=self.sunpath_toggle,
                delegate_3=self.sunlight_toggle,
                delegate_4=self.update_viewport_scene,
                width=360,
                height=590,
            )
            self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
        elif self._window:
            self._window.visible = False
