__all__ = ["SunpathExtension"]

import carb
import omni.ext
import omni.ui as ui
from omni.kit.viewport.utility import get_active_viewport_window
from .viewport_scene import ViewportScene
from .sunpath_data import SunpathData
from .sunlight_manipulator import SunlightManipulator


NVIDIACOLOR = 0xFF00B976
GRAY = 0xFFC1CDCD


class SunpathExtension(omni.ext.IExt):
    def __init__(self):
        self._viewport_scene = None
        self._scene_toggle = False
        self._sunlight_toggle = False
        self._scene_scale = 1
        self._scene_model = SunpathData(230, 12, 30, 112.94, 28.12)
        self._sunlight_model = SunlightManipulator(self._scene_model, self._scene_scale)

    def on_startup(self, ext_id):

        viewport_window = get_active_viewport_window()
        self._window = ui.Window("SunPath", width=370, height=310)

        if not viewport_window:
            carb.log_error(f"No Viewport Window to add {ext_id} scene to")
            return

        def sunpath_toggle(value):
            if value:
                self._scene_toggle = value
                self._viewport_scene = ViewportScene(viewport_window, ext_id, self._scene_scale, self._scene_model)
            else:
                self._scene_toggle = value
                self._viewport_scene.destroy()
                self._viewport_scene = None

        def sunlight_toggle(value):
            if value:
                self._sunlight_toggle = value
                self._sunlight_model.show_sun()
            else:
                self._sunlight_toggle = value
                self._sunlight_model.del_sun()

        def sunpath_change(valtype, value):
            if valtype is None:
                pass
            if valtype == "scale":
                self._scene_scale = value
            if valtype == "longitude":
                self._scene_model.set_longitude(value)
            if valtype == "latitude":
                self._scene_model.set_latitude(value)
            if valtype == "date":
                self._scene_model.set_date(value)
            if valtype == "hour":
                self._scene_model.set_hour(value)
            if valtype == "minite":
                self._scene_model.set_min(value)

            if self._sunlight_toggle:
                self._sunlight_model = SunlightManipulator(self._scene_model, self._scene_scale)
                self._sunlight_model.path = "/World/DistantLight"
                self._sunlight_model.show_sun()
            if self._scene_toggle:
                self._viewport_scene = ViewportScene(viewport_window, ext_id, self._scene_scale, self._scene_model)

        def label_info_change(valtype, value):
            if valtype == "longitude":
                self._scene_model.set_longitude(value)
            if valtype == "latitude":
                self._scene_model.set_latitude(value)
            if valtype == "date":
                self._scene_model.set_date(value)
            if valtype == "hour":
                self._scene_model.set_hour(value)
            if valtype == "minite":
                self._scene_model.set_min(value)
            dt_label.text = f"Datetime:   {self._scene_model.get_cur_time()}"
            sr_label.text = f"Sunrise:      {self._scene_model.get_sunrise_time()}"
            ss_label.text = f"Sunset:       {self._scene_model.get_sunset_time()}"

        with self._window.frame:
            with ui.VStack(style={"margin": 2}):
                with ui.HStack(
                    height=20,
                    style={
                        "Label": {"color": GRAY, "font_size": 16},
                        "CheckBox": {"background_color": NVIDIACOLOR},
                    },
                ):
                    ui.Label("Show Path", width=ui.Percent(25))
                    ui.Spacer(width=6)
                    turn_off = ui.CheckBox(width=60).model
                    turn_off.add_value_changed_fn(lambda m: sunpath_toggle(m.get_value_as_bool()))
                    ui.Spacer(width=6)

                    dt_label = ui.Label(
                        f"Datetime:   {self._scene_model.get_cur_time()}", style={"color": NVIDIACOLOR, "font_size": 14}
                    )
                with ui.HStack(
                    height=20,
                    style={
                        "Label": {"color": GRAY, "font_size": 16},
                        "CheckBox": {"background_color": NVIDIACOLOR},
                    },
                ):
                    ui.Label("Show   Sun", width=ui.Percent(25))
                    ui.Spacer(width=6)
                    turn_off = ui.CheckBox(width=60).model
                    turn_off.add_value_changed_fn(lambda m: sunlight_toggle(m.get_value_as_bool()))
                    ui.Spacer(width=6)

                    sr_label = ui.Label(
                        f"Sunrise:      {self._scene_model.get_sunrise_time()}",
                        style={"color": NVIDIACOLOR, "font_size": 14},
                    )
                with ui.HStack(
                    height=20,
                    style={
                        "Label": {"color": GRAY, "font_size": 16},
                        "CheckBox": {"background_color": NVIDIACOLOR},
                    },
                ):
                    ui.Label("Show Scale", width=ui.Percent(25))
                    ui.Spacer(width=5)
                    scale_drag = ui.FloatDrag(height=15, width=60, step=0.01).model
                    scale_drag.set_value(1)
                    scale_drag.add_value_changed_fn(lambda m: sunpath_change("scale", m.get_value_as_float()))
                    ui.Spacer(width=6)

                    ss_label = ui.Label(
                        f"Sunset:       {self._scene_model.get_sunset_time()}",
                        style={"color": NVIDIACOLOR, "font_size": 14},
                    )

                with ui.VStack(height=20):
                    ui.Line(
                        name="default",
                        style={
                            "border_width": 1,
                        },
                    )

                with ui.HStack(height=ui.Percent(20)):
                    with ui.VStack(width=ui.Percent(25), alignment=ui.Alignment.LEFT_CENTER):
                        ui.Label("Longitude")
                        ui.Label("Latitude")
                        ui.Label("Date")
                        ui.Label("Hour")
                        ui.Label("Minite")
                    with ui.VStack(height=ui.Percent(20)):
                        with ui.HStack():
                            field_2 = ui.FloatDrag(width=60, step=0.01)
                            ui.Spacer(width=6)
                            lon_drag = ui.FloatSlider(
                                min=-180,
                                max=180,
                                step=0.01,
                                model=field_2.model,
                                style={
                                    "color": 0x000000,
                                    "draw_mode": ui.SliderDrawMode.HANDLE,
                                    "secondary_selected_color": NVIDIACOLOR,
                                },
                            ).model
                            lon_drag.set_value(112.94)
                            lon_drag.add_value_changed_fn(lambda m: sunpath_change("longitude", m.get_value_as_float()))
                            lon_drag.add_value_changed_fn(
                                lambda m: label_info_change("longitude", m.get_value_as_float())
                            )
                        with ui.HStack():
                            field_3 = ui.FloatDrag(width=60, step=0.1)
                            ui.Spacer(width=6)
                            lat_drag = ui.FloatSlider(
                                min=-90,
                                max=90,
                                step=0.01,
                                model=field_3.model,
                                style={
                                    "color": 0x000000,
                                    "draw_mode": ui.SliderDrawMode.HANDLE,
                                    "secondary_selected_color": NVIDIACOLOR,
                                },
                            ).model
                            lat_drag.set_value(28.12)
                            lat_drag.add_value_changed_fn(lambda m: sunpath_change("latitude", m.get_value_as_float()))
                            lat_drag.add_value_changed_fn(
                                lambda m: label_info_change("latitude", m.get_value_as_float())
                            )
                        with ui.HStack():
                            field_4 = ui.IntDrag(width=60)
                            ui.Spacer(width=6)
                            date_drag = ui.IntSlider(
                                min=1,
                                max=365,
                                model=field_4.model,
                                style={
                                    "color": 0x000000,
                                    "draw_mode": ui.SliderDrawMode.HANDLE,
                                    "secondary_selected_color": NVIDIACOLOR,
                                },
                            ).model
                            date_drag.set_value(230)
                            date_drag.add_value_changed_fn(lambda m: sunpath_change("date", m.get_value_as_int()))
                            date_drag.add_value_changed_fn(lambda m: label_info_change("date", m.get_value_as_int()))
                        with ui.HStack():
                            field_5 = ui.IntDrag(width=60)
                            ui.Spacer(width=6)
                            hour_drag = ui.IntSlider(
                                min=0,
                                max=23,
                                model=field_5.model,
                                style={
                                    "color": 0x000000,
                                    "draw_mode": ui.SliderDrawMode.HANDLE,
                                    "secondary_selected_color": NVIDIACOLOR,
                                },
                            ).model
                            hour_drag.set_value(12)
                            hour_drag.add_value_changed_fn(lambda m: sunpath_change("hour", m.get_value_as_int()))
                            hour_drag.add_value_changed_fn(lambda m: label_info_change("hour", m.get_value_as_int()))
                        with ui.HStack():
                            field_6 = ui.IntDrag(width=60)
                            ui.Spacer(width=6)
                            minite_drag = ui.IntSlider(
                                min=0,
                                max=59,
                                model=field_6.model,
                                style={
                                    "color": 0x000000,
                                    "draw_mode": ui.SliderDrawMode.HANDLE,
                                    "secondary_selected_color": NVIDIACOLOR,
                                },
                            ).model
                            minite_drag.set_value(30)
                            minite_drag.add_value_changed_fn(lambda m: sunpath_change("minite", m.get_value_as_int()))
                            minite_drag.add_value_changed_fn(
                                lambda m: label_info_change("minite", m.get_value_as_int())
                            )

    def on_shutdown(self):
        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._sunlight_model.del_sun()
            self._viewport_scene = None
