# MIT License
# Copyright (c) 2017 John Bryan Moore
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""

"""

import time
import VL53L0X
from collections import deque


def average(lst):
    return sum(lst)/len(lst)


def init_tof(bus=1, address=0x29, min_time):
    tof = VL53L0X.VL53L0X(i2c_bus=bus, i2c_address=address)
    tof.open()
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
    timing = tof.get_timing()
    if timing < min_time:
        return tof, min_time
    else:
        return tof, timing


def main():
    tof, timing = init_tof()
    distance_array = deque([], maxlen=10)
    while True:
        distance = tof.get_distance()
        if len(distance_array) <= 9:
            distance_array.append(distance)
        elif distance > 0 and abs(distance - average(distance_array)) < 20:
            distance_array.append(distance)
            print("{} mm".format(average(distance_array)))
        time.sleep(timing/1000000.00)
    tof.stop_ranging()
    tof.close()


if __name__ == "__main__":
    main()
