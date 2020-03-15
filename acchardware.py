import os
import time


class AccHardware:
    _pos = "/sys/devices/platform/lis3lv02d/position"

    @staticmethod
    def acc_exists():
        return os.path.exists(AccHardware._pos) and os.path.isfile(AccHardware._pos)

    @staticmethod
    def get_values():
        with open(AccHardware._pos, "r") as position:
            s = position.readline().strip().strip("()").split(",")
            t = time.time()
            x = float(s[0]) / 1000.
            y = float(s[1]) / 1000.
            z = float(s[2]) / 1000.
            return t, x, y, z
