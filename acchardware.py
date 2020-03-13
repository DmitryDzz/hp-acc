import time


class AccHardware:
    @staticmethod
    def get_accelerometer_name():
        with open("/sys/devices/platform/lis3lv02d/input/input14/name", "r") as name:
            return name.readline().strip()

    @staticmethod
    def get_values():
        with open("/sys/devices/platform/lis3lv02d/position", "r") as position:
            s = position.readline().strip().strip("()").split(",")
            t = time.time()
            x = float(s[0]) / 1000.
            y = float(s[1]) / 1000.
            z = float(s[2]) / 1000.
            return t, x, y, z
