from math import sqrt
import time


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


def print_header(file):
    file.write("{}\t{}\t{}\t{}\t{}\n".format("time", "acc.x", "acc.y", "acc.z", "|acc|"))


def print_values(file, start_time):
    t = int(round(time.time() * 1000.)) - start_time
    values = get_values()
    x = values[0]
    y = values[1]
    z = values[2]
    m = sqrt(x * x + y * y + z * z)
    file.write("{}\t{}\t{}\t{}\t{}\n".format(t, x, y, z, m))


def main():
    print()
    print("Press Ctrl+C to exit")
    print()
    print("Device name: " + get_accelerometer_name())
    print()
    start_time = int(round(time.time() * 1000))
    with open("./hp-acc.csv", "w") as file:
        print_header(file)
        try:
            while True:
                print_values(file, start_time)
        except KeyboardInterrupt:
            pass
    print()


if __name__ == '__main__':
    main()
