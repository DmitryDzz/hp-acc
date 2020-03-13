import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from acchardware import AccHardware
from accfigure import AccFigure


def thread_function(_name, acc_figure_1, acc_figure_2):
    while True:
        t, x, y, z = AccHardware.get_values()
        acc_figure_1.feed_acc(t, x, y, z)
        acc_figure_2.feed_acc(t, x, y, z)


def animate(_i, acc_figure_1, acc_figure_2):
    f = acc_figure_1
    last_index = len(f.t_values) - 1
    if last_index < 0:
        return
    t = f.t_values[len(f.t_values) - 1]

    plt.cla()
    plt.plot(f.t_values, f.x_values, label="x axis", color="g")
    plt.plot(f.t_values, f.y_values, label="y axis", color="y")
    plt.plot(f.t_values, f.z_values, label="z axis", color="r")
    plt.plot(f.t_values, f.m_values, label="magnitude", color="k")

    plt.xlim(left=max(0., t-10), right=max(t, 10))

    y_bottom, y_top = plt.ylim()
    plt.ylim(bottom=min(-1.0, y_bottom), top=max(1.0, y_top))

    plt.title("Accelerometer data (rate={:.1f})".format(f.rate), loc="left")
    plt.legend(loc="lower left")
    plt.grid(True)
    # plt.tight_layout()


def main():
    acc_figure_1 = AccFigure(1.0)
    acc_figure_2 = AccFigure(0.2)

    print()
    print("Press Ctrl+C to exit")
    print()
    print("Device name: " + AccHardware.get_accelerometer_name())
    print()

    thread = threading.Thread(target=thread_function, args=(1, acc_figure_1, acc_figure_2), daemon=True)
    thread.start()

    # plt.style.use("fivethirtyeight")
    figure = plt.figure(num="Accelerometer data")
    figure.add_subplot(1, 1, 1)
    _animation = FuncAnimation(figure, animate, fargs=(acc_figure_1, acc_figure_2), interval=100)
    plt.show()


if __name__ == '__main__':
    main()
