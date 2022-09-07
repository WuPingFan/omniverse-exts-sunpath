__all__ = ["sunpath_window_style"]

from omni.ui import color as cl
from omni.ui import constant as fl
from omni.ui import url
import omni.kit.app
import omni.ui as ui
import pathlib

EXTENSION_FOLDER_PATH = pathlib.Path(
    omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__)
)

# Pre-defined constants. It's possible to change them runtime.
cl.slider_bg_color = cl(0.28, 0.28, 0.28, 0.0)
cl.window_bg_color = cl(0.2, 0.2, 0.2, 1.0)
cl.sunpath_window_attribute_bg = cl(0, 0, 0)
cl.sunpath_window_attribute_fg = cl(1.0, 1.0, 1.0, 0.3)
cl.sunpath_window_hovered = cl(0.95, 0.95, 0.95, 1.0)
cl.sunpath_window_item = cl(0.65, 0.65, 0.65, 1.0)

fl.sunpath_window_attr_hspacing = 15
fl.sunpath_window_attr_spacing = 1
fl.sunpath_window_group_spacing = 2
fl.border_radius = 3
fl.outer_frame_padding = 8

url.sunpath_window_icon_closed = f"{EXTENSION_FOLDER_PATH}/icons/closed.svg"
url.sunpath_window_icon_opened = f"{EXTENSION_FOLDER_PATH}/icons/opened.svg"

url.diag_bg_lines_texture = f"{EXTENSION_FOLDER_PATH}/icons/diagonal_texture.png"
url.button_update = f"{EXTENSION_FOLDER_PATH}/icons/update.png"
url.extension_tittle = f"{EXTENSION_FOLDER_PATH}/icons/window_tittle.png"
extension_tittle = f"{EXTENSION_FOLDER_PATH}/icons/test.png"

# The main style dict
sunpath_window_style = {
    "CheckBox": {
        "background_color": cl.sunpath_window_item,
        "selected_color": cl.beige,
    },
    "CheckBox:hovered": {"background_color": cl.beige},
    "Button": {
        "background_color": cl.sunpath_window_attribute_fg,
        "border_radius": 4,
        "margin_height": 2,
        "margin_width": 10,
        "padding": 2,
    },
    "Button:hovered": {"background_color": cl.beige},
    "Button:pressed": {"background_color": cl.sunpath_window_item},
    "Button.Label": {"alignment": ui.Alignment.CENTER_BOTTOM},
    "Button.Image::attribute_set": {
        "image_url": url.button_update,
    },
    "Label::attribute_name": {
        "font_size": 14,
        "color": cl.sunpath_window_item,
        "alignment": ui.Alignment.RIGHT_CENTER,
        "margin_height": fl.sunpath_window_attr_spacing,
        "margin_width": fl.sunpath_window_attr_hspacing,
    },
    "CollapsableFrame::group": {
        "margin_height": 5,
        "background_color": cl.slider_bg_color,
    },
    "ScrollingFrame::window_bg": {
        "background_color": cl.window_bg_color,
        "padding": fl.outer_frame_padding,
        "border_radius": 20,
    },
    "Label::attribute_name:hovered": {"color": cl.sunpath_window_hovered},
    "Label::collapsable_name": {"alignment": ui.Alignment.LEFT_CENTER},
    "HeaderLine": {"color": cl(0.5, 0.5, 0.5, 0.5)},
    "Slider": {
        "background_color": cl.slider_bg_color,
        "secondary_color": cl.beige,
        "secondary_selected_color": cl.sunpath_window_item,
        "color": 0x00000000,
        "draw_mode": ui.SliderDrawMode.HANDLE,
        "border_radius": fl.border_radius,
        "corner_flag": ui.CornerFlag.LEFT,
        "margin_height": 4,
    },
    "Image::slider_bg_texture": {
        "image_url": url.diag_bg_lines_texture,
        "border_radius": fl.border_radius,
        "margin_height": 13,
    },
    "Field": {
        "background_color": 0x00000000,
        "color": cl.sunpath_window_item,
        "margin_height": 4,
        "margin_width": 5,
        "border_radius": fl.border_radius,
    },
    "Image::extension_tittle": {"image_url": url.extension_tittle, "margin": 10},
    "Image::collapsable_opened": {"color": cl.sunpath_window_item, "image_url": url.sunpath_window_icon_opened},
    "Image::collapsable_closed": {"color": cl.sunpath_window_item, "image_url": url.sunpath_window_icon_closed},
}
