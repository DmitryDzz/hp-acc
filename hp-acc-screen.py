from math import sqrt
from time import sleep


def get_accelerometer_name():
    with open("/sys/devices/platform/lis3lv02d/input/input14/name", "r") as name:
        return name.readline().strip()


def get_values():
    with open("/sys/devices/platform/lis3lv02d/position", "r") as position:
        s = position.readline().strip().strip("()").split(",")
        x = float(s[0]) / 1000.
        y = float(s[1]) / 1000.
        z = float(s[2]) / 1000.
        return x, y, z


def print_header():
    print("{:10}{:10}{:10}{:10}".format("acc.x".rjust(10), "acc.y".rjust(10), "acc.z".rjust(10), "|acc|".rjust(10)))
    print("{:10}{:10}{:10}{:10}".format("-----".rjust(10), "-----".rjust(10), "-----".rjust(10), "-----".rjust(10)))


def print_values():
    values = get_values()
    x = values[0]
    y = values[1]
    z = values[2]
    m = sqrt(x * x + y * y + z * z)
    print("\r{:10.3f}{:10.3f}{:10.3f}{:10.3f}".format(x, y, z, m), end="")


def main():
    print()
    print("Press Ctrl+C to exit")
    print()
    print("Device name: " + get_accelerometer_name())
    print()
    print_header()
    try:
        while True:
            print_values()
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    print()


if __name__ == '__main__':
    main()
