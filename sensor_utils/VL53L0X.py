# !/usr/bin/env python3

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

import time
import VL53L0X
from collections import deque
import logging
from scipy.interpolate import interp1d


class ToFSensor:
    """
        Returns measured distance of VL53L0X sensor, based on John Bryan Moore
        library:
            https://github.com/johnbryanmoore/VL53L0X_rasp_python
        Distance values bounces because sensor inaccuracy. Using a dynamic
        accuracy the variance
        is reduced. Calibration is an option too.
        args:
            tof: ToF object from VL53L0X libary
            timing: ¿¿??
            distance_array: queue for dynamic average storage
            interpolate: function to interpolate measure to real values
            (offset)
                TODO: config file for interpolation values
            calibrate: use interpolate function or not
    """
    def __init__(self, address=0x29, array_size=10, calibrated=False):
        self.tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=address)
        self.timing = self._set_timing()
        self.distance_array = deque([], maxlen=array_size)
        self.interpolate = self.calibrate()
        self.calibrated = calibrated

    def _set_timing(self):
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        timing = self.tof.get_timing()
        if timing < 20000:
            return 20000
        else:
            return timing

    def calibrate(self):
        real = [i for i in range(0, 100, 10)]
        sensor = [i for i in range(0, 100, 10)]
        return interp1d(real, sensor, kind='cubic')

    def average(self):
        return sum(self.distance_array)/len(self.distance_array)

    def get_distance(self):
        if self.calibrated:
            return self.interpolate(self.tof.get_distance())
        else:
            return self.tof.get_distance()

    def calculate_average_distance(self, array_size=10):
        distance = self.get_distance()
        if len(self.distance_array) <= self.distance_array.maxlen:
            self.distance_array.append(distance)
        elif distance > 0:
            self.distance_array.append(distance)
            logging.info("{} mm".format(self.average()))
        time.sleep(self.timing/1000000.00)

    def stop(self):
        self.tof.stop_ranging()
        self.tof.close()


def main():
    tof = ToFSensor()
    try:
        while True:
            tof.calculate_average_distance()
            tof_distance = tof.average()
            print("Distance: ", tof_distance)
            time.sleep(.5)
    finally:
        tof.stop()


if __name__ == '__main__':
    main()
