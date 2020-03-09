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
        m = sqrt(x * x + y * y + z * z)
        return t, x, y, z, m


t_values = []
x_values = []
y_values = []
z_values = []
m_values = []

start_t = 0


def animate(i):
    t, x, y, z, m = get_values()

    global start_t
    if i == 0:
        start_t = t
    t = t - start_t

    t_values.append(t)
    x_values.append(x)
    y_values.append(y)
    z_values.append(z)
    m_values.append(m)
    plt.cla()
    plt.plot(t_values, x_values, label="x axis", color="g")
    plt.plot(t_values, y_values, label="y axis", color="y")
    plt.plot(t_values, z_values, label="z axis", color="r")
    plt.plot(t_values, m_values, label="magnitude", color="k")

    plt.xlim(left=max(0., t-10), right=max(t, 10))

    y_bottom, y_top = plt.ylim()
    plt.ylim(bottom=min(-1.0, y_bottom), top=max(1.0, y_top))

    plt.legend(loc="upper left")
    plt.tight_layout()


def main():
    print()
    print("Press Ctrl+C to exit")
    print()
    print("Device name: " + get_accelerometer_name())
    print()
    # plt.style.use("fivethirtyeight")
    animation = FuncAnimation(plt.gcf(), animate, interval=1)
    plt.show()


if __name__ == '__main__':
    main()
