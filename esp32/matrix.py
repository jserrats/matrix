import machine
import neopixel
import time

red = (100, 0, 0)


class Matrix:
    width = 32
    height = 32
    num_leds = height * width
    pin = 15

    def __init__(self):
        self.np = neopixel.NeoPixel(machine.Pin(self.pin), self.num_leds)
        self.clear()

    def __setitem__(self, coordinates, color):
        x, y = coordinates
        self.np[self._xy2i(x, y)] = color

    def _i2xy(self, len):
        y = len//Matrix.height
        if y % 2 == 0:
            x = Matrix.width - ((len % Matrix.width)+1)
        else:
            x = len % Matrix.width
        return x, y

    def _xy2i(self, x, y):
        return y*self.width + (y % 2)*x + ((y+1) % 2)*(Matrix.width - x - 1)

    def clear(self):
        for i in range(self.num_leds):
            self.np[i] = (0, 0, 0)
        self.write()

    def startup_animation(self):
        for i in range(0, self.height):
            for ii in range(i):
                self[i-1-ii, ii] = (0, 100, 100)
                self[ii, ii - i] = (0, 100, 100)
                self[32 - (i-1-ii), ii] = (0, 100, 100)
                self[32 - ii, ii - i] = (0, 100, 100)
            self.write()
        self[16, 16] = (0, 100, 100)
        self[16, 15] = (0, 100, 100)
        self.write()
        time.sleep(5)

    def startup_animation_finish(self):
        for i in reversed(range(self.height)):
            for ii in range(i):
                self[i-1-ii, ii] = (0, 0, 0)
                self[ii, ii - i] = (0, 0, 0)
                self[32 - (i-1-ii), ii] = (0, 0, 0)
                self[32 - ii, ii - i] = (0, 0, 0)
            self.write()

        self.clear()

    def write(self):
        self.np.write()
