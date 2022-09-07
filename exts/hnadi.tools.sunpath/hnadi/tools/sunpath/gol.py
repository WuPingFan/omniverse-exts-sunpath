"""Build global dictionary"""

from .sunpath_data import SunpathData


def _init():
    global _global_dict
    _global_dict = {}

    # Pathmodel For draw sphere
    _global_dict["pathmodel"] = SunpathData(230, 12, 30, 112.94, 28.12)

    # For distant light to determine whether to change the attribute
    _global_dict["dome_angle"] = None

    # Parameter for DrawSunpath
    _global_dict["origin"] = [0, 0, 0]
    _global_dict["scale"] = 50
    _global_dict["color"] = [255, 255, 255]
    _global_dict["length"] = 3.5

    # Flag for show sun
    _global_dict["sun_state"] = False
    # Flag for show info
    _global_dict["show_info"] = False


def set_value(key, value):
    _global_dict[key] = value


def set_item(key, i, value):
    _global_dict[key][i] = value


def get_value(key):
    try:
        return _global_dict[key]
    except:
        print("get" + key + "fail\r\n")
