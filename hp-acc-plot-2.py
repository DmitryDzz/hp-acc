import struct
import threading
import time
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_accelerometer_name():
    with open("/sys/devices/platform/lis3lv02d/input/input14/name", "r") as name:
        return name.readline().strip()


def get_values():
    with open("/sys/devices/platform/lis3lv02d/position", "r") as position:
        s = position.readline().strip().strip("()").split(",")
        t = time.time()
        x = float(s[0]) / 1000.
        y = float(s[1]) / 1000.
        z = float(s[2]) / 1000.
        return t, x, y, z


def lerp(v0, v1, alpha):
    return v0 + alpha * (v1 - v0)


t_values = []
x_values = []
y_values = []
z_values = []
m_values = []

start_t = None

rate = 0.0


def thread_function_1(_name):
    global rate

    prev_x = None
    prev_y = None
    prev_z = None

    i = 0

    while True:
        t, x, y, z = get_values()

        global start_t
        if start_t is None:
            start_t = t
        t = t - start_t
        rate = 0 if t < 0.001 else i / t
        i += 1

        # alpha = 0.2
        alpha = 1.0
        # alpha = 0.6
        x = x if prev_x is None else lerp(prev_x, x, alpha)
        y = y if prev_y is None else lerp(prev_y, y, alpha)
        z = z if prev_z is None else lerp(prev_z, z, alpha)
        prev_x = x
        prev_y = y
        prev_z = z
        m = sqrt(x * x + y * y + z * z)

        t_values.append(t)
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)
        m_values.append(m)

        # time.sleep(0.01)


def thread_function_2(_name):
    global rate

    prev_x = None
    prev_y = None
    prev_z = None

    i = 0

    with open("/dev/input/event12", "rb") as device:
        x = y = z = 0
        while True:
            data = device.read(24)  # Reads 24 bytes
            s = struct.unpack("4IHHi", data)
            tp = s[4]

            if tp == 3:
                t = float(s[0]) + float(s[2]) / 1000000.
                global start_t
                if start_t is None:
                    start_t = t
                t = t - start_t
                rate = 0 if t < 0.001 else i / t
                i += 1

                code = s[5]
                value = float(s[6]) / 1000.
                if code == 0:
                    x = value
                elif code == 1:
                    y = value
                elif code == 2:
                    z = value
            elif tp == 0:
                # alpha = 0.2
                alpha = 1.0
                # alpha = 0.6
                x = x if prev_x is None else lerp(prev_x, x, alpha)
                y = y if prev_y is None else lerp(prev_y, y, alpha)
                z = z if prev_z is None else lerp(prev_z, z, alpha)
                prev_x = x
                prev_y = y
                prev_z = z
                m = sqrt(x * x + y * y + z * z)

                t_values.append(t)
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)
                m_values.append(m)


def animate(_i):
    last_index = len(t_values) - 1
    if last_index < 0:
        return
    t = t_values[len(t_values) - 1]

    plt.cla()
    plt.plot(t_values, x_values, label="x axis", color="g")
    plt.plot(t_values, y_values, label="y axis", color="y")
    plt.plot(t_values, z_values, label="z axis", color="r")
    plt.plot(t_values, m_values, label="magnitude", color="k")

    plt.xlim(left=max(0., t-10), right=max(t, 10))

    y_bottom, y_top = plt.ylim()
    plt.ylim(bottom=min(-1.0, y_bottom), top=max(1.0, y_top))

    plt.title("Accelerometer data (rate={:.1f})".format(rate), loc="left")
    plt.legend(loc="lower left")
    plt.grid(True)
    # plt.tight_layout()


def main():
    print()
    print("Press Ctrl+C to exit")
    print()
    print("Device name: " + get_accelerometer_name())
    print()

    thread = threading.Thread(target=thread_function_1, args=(1,), daemon=True)
    # thread = threading.Thread(target=thread_function_2, args=(1,), daemon=True)
    thread.start()

    # plt.style.use("fivethirtyeight")
    figure = plt.figure(num="Accelerometer data")
    figure.add_subplot(1, 1, 1)
    _animation = FuncAnimation(figure, animate, interval=100)
    plt.show()


if __name__ == '__main__':
    main()
