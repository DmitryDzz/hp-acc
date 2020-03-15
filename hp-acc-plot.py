import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from acchardware import AccHardware
from accfigure import AccFigure


def thread_function(_name, acc_figure):
    while True:
        t, x, y, z = AccHardware.get_values()
        acc_figure.feed_acc(t, x, y, z)


def animate(_i, acc_figure):
    last_index = len(acc_figure.t_values) - 1
    if last_index < 0:
        return
    t = acc_figure.t_values[len(acc_figure.t_values) - 1]

    plt.cla()
    plt.plot(acc_figure.t_values, acc_figure.x_values, label="x axis", color="g")
    plt.plot(acc_figure.t_values, acc_figure.y_values, label="y axis", color="y")
    plt.plot(acc_figure.t_values, acc_figure.z_values, label="z axis", color="r")
    plt.plot(acc_figure.t_values, acc_figure.m_values, label="magnitude", color="k")

    plt.xlim(left=max(0., t-10), right=max(t, 10))

    y_bottom, y_top = plt.ylim()
    plt.ylim(bottom=min(-1.0, y_bottom), top=max(1.0, y_top))

    plt.title("Accelerometer data (rate={:.1f})".format(acc_figure.rate), loc="left")
    plt.legend(loc="lower left")
    plt.grid(True)
    # plt.tight_layout()


def main():
    print()
    if not AccHardware.acc_exists():
        print("Accelerometer not found")
        print()
        return -1

    print("Press Ctrl+C to exit")
    print()

    acc_figure = AccFigure(1.0)
    thread = threading.Thread(target=thread_function, args=(1, acc_figure), daemon=True)
    thread.start()

    # plt.style.use("fivethirtyeight")
    figure = plt.figure(num="Accelerometer data")
    figure.add_subplot(1, 1, 1)
    _animation = FuncAnimation(figure, animate, fargs=(acc_figure,), interval=100)
    plt.show()

    return 0


if __name__ == '__main__':
    main()
