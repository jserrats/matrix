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
        for i in range(self.num_leds):
            self.np[i] = (0, 150, 150)
            if i % self.width == 0:
                self.write()

    def startup_animation_finish(self):
        for i in range(32):
            self[0, i] = red
            self[i, 0] = red
            self[31, i] = red
            self[i, 31] = red

        self.write()
        time.sleep(0.5)
        self.clear()

    def write(self):
        self.np.write()
