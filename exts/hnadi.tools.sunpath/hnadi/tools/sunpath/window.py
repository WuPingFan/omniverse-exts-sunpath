__all__ = ["SunpathWindow"]

import omni.ui as ui
from functools import partial
from .style import sunpath_window_style
from . import gol


LABEL_WIDTH = 120
SPACING = 4


class SunpathWindow(ui.Window):
    """The class that represents the window"""

    def __init__(self, title: str, delegate_1=None, delegate_2=None, delegate_3=None, delegate_4=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        # Apply the style to all the widgets of this window
        self.frame.style = sunpath_window_style

        # Set the function that is called to build widgets when the window is visible
        self.frame.set_build_fn(self._build_fn)

        # Methods to change parameters and update viewport secene
        self.update = delegate_1
        self.show_path = delegate_2
        self.show_sun = delegate_3
        self.update_scene = delegate_4

    def destroy(self):
        # It will destroy all the children
        super().destroy()

    @property
    def label_width(self):
        """The width of the attribute label"""
        return self.__label_width

    @label_width.setter
    def label_width(self, value):
        """The width of the attribute label"""
        self.__label_width = value
        self.frame.rebuild()

    def _build_collapsable_header(self, collapsed, title):
        """Build a custom title of CollapsableFrame"""
        with ui.VStack():
            ui.Spacer(height=8)
            with ui.HStack():
                ui.Label(title, name="collapsable_name")

                if collapsed:
                    image_name = "collapsable_opened"
                else:
                    image_name = "collapsable_closed"
                ui.Image(name=image_name, width=10, height=10)
            ui.Spacer(height=8)
            ui.Line(style_type_name_override="HeaderLine")

    def _build_display(self):
        """Build the widgets of the "display" group"""
        with ui.CollapsableFrame("display".upper(), name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=8)
                with ui.HStack():
                    with ui.VStack():
                        with ui.HStack():
                            ui.Label("Show Path", name="attribute_name", width=self.label_width)
                            sp = ui.CheckBox(name="attribute_bool").model
                            sp.add_value_changed_fn(lambda m: self.show_path(m.get_value_as_bool()))
                        ui.Spacer(height=8)
                        with ui.HStack():
                            ui.Label("Show Sun", name="attribute_name", width=self.label_width)
                            ss = ui.CheckBox(name="attribute_bool").model
                            ss.add_value_changed_fn(lambda m: self.show_sun(m.get_value_as_bool()))
                            ss.add_value_changed_fn(lambda m: self.update_scene())
                        ui.Spacer(height=8)
                        with ui.HStack():
                            ui.Label("Show Info", name="attribute_name", width=self.label_width)
                            si = ui.CheckBox(name="attribute_bool").model
                            si.add_value_changed_fn(lambda m: self.update("show_info", m.get_value_as_bool()))
                    with ui.ZStack():
                        ui.Image(
                            name="extension_tittle",
                            fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                            width=ui.Percent(100),
                        )
                ui.Spacer(height=8)
                with ui.HStack():
                    ui.Label("Path Color", name="attribute_name", width=self.label_width)
                    color_model = ui.ColorWidget(1, 1, 1, width=0, height=0).model
                    r_model = color_model.get_item_children()[0]
                    r_component = color_model.get_item_value_model(r_model)
                    r_component.add_value_changed_fn(lambda m: gol.set_item("color", 0, m.get_value_as_float()))
                    g_model = color_model.get_item_children()[1]
                    g_component = color_model.get_item_value_model(g_model)
                    g_component.add_value_changed_fn(lambda m: gol.set_item("color", 1, m.get_value_as_float()))
                    b_model = color_model.get_item_children()[2]
                    b_component = color_model.get_item_value_model(b_model)
                    b_component.add_value_changed_fn(lambda m: gol.set_item("color", 2, m.get_value_as_float()))
                    ui.Spacer()
                    ui.Button(
                        name="attribute_set",
                        tooltip="update color or update scene",
                        width=60,
                        clicked_fn=partial(self.update, None, None),
                    )
                ui.Spacer(height=4)
                with ui.HStack():
                    ui.Label("Path Scale", name="attribute_name", width=self.label_width)
                    with ui.ZStack():
                        ui.Image(name="slider_bg_texture", fill_policy=ui.FillPolicy.STRETCH, width=ui.Percent(100))
                        ps_slider = ui.FloatSlider(name="attribute_slider", min=1, max=100, setp=1).model
                        ps_slider.set_value(50)
                        ps_slider.add_value_changed_fn(lambda m: self.update("scale", m.get_value_as_float()))
                    ui.FloatField(model=ps_slider, width=60)

    def _build_location(self):
        """Build the widgets of the "location" group"""
        with ui.CollapsableFrame("location".upper(), name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=8)
                with ui.HStack():
                    ui.Label("Longitude", name="attribute_name", width=self.label_width)
                    with ui.ZStack():
                        ui.Image(name="slider_bg_texture", fill_policy=ui.FillPolicy.STRETCH, width=ui.Percent(100))
                        lon_slider = ui.FloatSlider(name="attribute_slider", min=-180, max=180, setp=0.01).model
                        lon_slider.set_value(112.22)
                        lon_slider.add_value_changed_fn(lambda m: self.update("longitude", m.get_value_as_float()))
                    ui.FloatField(model=lon_slider, width=60)
                ui.Spacer(height=2)
                with ui.HStack():
                    ui.Label("Latitude", name="attribute_name", width=self.label_width)
                    with ui.ZStack():
                        ui.Image(
                            name="slider_bg_texture",
                            fill_policy=ui.FillPolicy.STRETCH,
                            width=ui.Percent(100),
                        )
                        lat_slider = ui.FloatSlider(name="attribute_slider", min=-90, max=90, step=0.01).model
                        lat_slider.set_value(22.22)
                        lat_slider.add_value_changed_fn(lambda m: self.update("latitude", m.get_value_as_float()))
                    ui.FloatField(model=lat_slider, width=60)

    def _build_datetime(self):
        """Build the widgets of the "datetime" group"""
        with ui.CollapsableFrame("datetime".upper(), name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=8)
                with ui.HStack():
                    ui.Label("Date", name="attribute_name", width=self.label_width)
                    with ui.ZStack():
                        ui.Image(
                            name="slider_bg_texture",
                            fill_policy=ui.FillPolicy.STRETCH,
                            width=ui.Percent(100),
                        )
                        dt_slider = ui.IntSlider(
                            name="attribute_slider",
                            min=1,
                            max=365,
                        ).model
                        dt_slider.set_value(175)
                        dt_slider.add_value_changed_fn(lambda m: self.update("date", m.get_value_as_int()))
                    ui.IntField(model=dt_slider, width=60)
                ui.Spacer(height=2)
                with ui.HStack():
                    ui.Label("Hour", name="attribute_name", width=self.label_width)
                    with ui.ZStack():
                        ui.Image(
                            name="slider_bg_texture",
                            fill_policy=ui.FillPolicy.STRETCH,
                            width=ui.Percent(100),
                        )
                        hr_slider = ui.IntSlider(name="attribute_slider", min=0, max=23).model
                        hr_slider.set_value(12)
                        hr_slider.add_value_changed_fn(lambda m: self.update("hour", m.get_value_as_int()))
                    ui.IntField(model=hr_slider, width=60)
                ui.Spacer(height=2)
                with ui.HStack():
                    ui.Label("Minite", name="attribute_name", width=self.label_width)
                    with ui.ZStack():
                        ui.Image(
                            name="slider_bg_texture",
                            fill_policy=ui.FillPolicy.STRETCH,
                            width=ui.Percent(100),
                        )
                        mt_slider = ui.IntSlider(name="attribute_slider", min=0, max=59).model
                        mt_slider.set_value(30)
                        mt_slider.add_value_changed_fn(lambda m: self.update("minite", m.get_value_as_int()))
                    ui.IntField(model=mt_slider, width=60)

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is visible.
        """
        with ui.ScrollingFrame(name="window_bg", horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF):
            with ui.ScrollingFrame():
                with ui.VStack(height=0):
                    self._build_display()
                    self._build_location()
                    self._build_datetime()
