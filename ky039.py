import time
import board
import busio
from collections import deque
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

class KY039:
    def __init__(self, channel=0):
        i2c = busio.I2C(board.SCL, board.SDA)
        self._ads = ADS1115(i2c)
        self._chan = AnalogIn(self._ads, channel)
        self._last_beat = time.time()
        self._bpm = 0
        self._buffer = deque(maxlen=10) 
        self._prev_avg = 0
        self._rising = False

    def read(self):
        return self._chan.value

    def _smooth(self, value):
        self._buffer.append(value)
        return sum(self._buffer) / len(self._buffer)

    def read_bpm(self):
        raw = self.read()
        avg = self._smooth(raw)
        diff = avg - self._prev_avg

        if diff > 800 and not self._rising:
            self._rising = True
            now = time.time()
            interval = now - self._last_beat
            if 0.4 < interval < 1.5: 
                self._bpm = int(60 / interval)
            self._last_beat = now

        if diff < -300:
            self._rising = False

        self._prev_avg = avg
        return self._bpm, int(avg)
