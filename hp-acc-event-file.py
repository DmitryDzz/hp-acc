import struct
from math import sqrt


def get_accelerometer_name():
    with open("/sys/devices/platform/lis3lv02d/input/input14/name", "r") as name:
        return name.readline().strip()


def print_header(output_file):
    output_file.write("{}\t{}\t{}\t{}\t{}\n".format("time", "acc.x", "acc.y", "acc.z", "|acc|"))


'''
struct input_event {
    struct timeval time; // 16 bytes
    unsigned short type; // 2 bytes
    unsigned short code; // 2 bytes
    unsigned int value;  // 4 bytes
};
// 24 bytes total
'''


def print_data(output_file):
    with open("/dev/input/event12", "rb") as device:
        try:
            x = y = z = 0
            while True:
                data = device.read(24)  # Reads 24 bytes
                s = struct.unpack("4IHHi", data)
                tp = s[4]

                if tp == 3:
                    timestamp = float(s[0]) + float(s[2]) / 1000000.
                    code = s[5]
                    value = float(s[6]) / 1000.
                    if code == 0:
                        x = value
                    elif code == 1:
                        y = value
                    elif code == 2:
                        z = value
                elif tp == 0:
                    m = sqrt(x * x + y * y + z * z)
                    output_file.write("{}\t{}\t{}\t{}\t{}\n".format(timestamp, x, y, z, m))
        except KeyboardInterrupt:
            pass
    print()


def main():
    print()
    print("Press Ctrl+C to exit")
    print()
    print("Device name: " + get_accelerometer_name())
    print()
    with open("./hp-acc-event.csv", "w") as file:
        print_header(file)
        print_data(file)


if __name__ == '__main__':
    main()
