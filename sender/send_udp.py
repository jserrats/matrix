import socket
import json
from PIL import Image, ImageEnhance
import time
import sys

UDP_IP = "matrix.lan"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP


size = (32, 32)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def process_image(im):
    im = crop_max_square(im)
    out = im.resize(size, Image.Resampling.LANCZOS)
    brightness = ImageEnhance.Brightness(out)
    out = brightness.enhance(0.05)

    saturation = ImageEnhance.Color(out)
    out = saturation.enhance(2)

    contrast = ImageEnhance.Contrast(out)
    out = contrast.enhance(2)

    return out
# out.save('resize-output.png')


def send_image(im):
    bin_image = im.tobytes()
    msg = b''

    def i2xy(i):
        y = 31 - i//32
        x = i % 32
        return x, y

    for i, j in zip(range(0, len(bin_image), 3), range(1024)):
        pixel = []
        for color in bin_image[i:i + 3]:
            pixel.append(int(color)//2)
        x, y = i2xy(j)
        msg += bytes([x, y] + pixel)

    max_pixels_per_packet = 1024//5 +1
    print(
        f'max pixels pp {max_pixels_per_packet} - npackets {len(msg)/max_pixels_per_packet}')
    for i in range(0, len(msg), max_pixels_per_packet):
        print(f'i={i}')
        msgb = b''

        print(msg[i:i + max_pixels_per_packet])
        # packet
        pixels_in_packet = msg[i:i + max_pixels_per_packet]
        for j in range(0, len(pixels_in_packet), 5):
            print(pixels_in_packet[j:j+5],bytes(pixels_in_packet[j:j+5]))
            msgb += bytes(pixels_in_packet[j:j+5])
        sock.sendto(msgb, (UDP_IP, UDP_PORT))
        #return
        time.sleep(0.05)


def send_test():
    msg = []
    for i in range(32):
        for j in range(32):
            msg += bytes([i, j, 0, 0, 100])

    max_pixels_per_packet = 1024//5 +1
    print(
        f'max pixels pp {max_pixels_per_packet} - npackets {len(msg)/max_pixels_per_packet}')
    for i in range(0, len(msg), max_pixels_per_packet):
        #print(f'i={i}')
        msgb = b''

        #print(msg[i:i + max_pixels_per_packet])
        # packet
        pixels_in_packet = msg[i:i + max_pixels_per_packet]
        for j in range(0, len(pixels_in_packet), 5):
            #print(pixels_in_packet[j:j+5],bytes(pixels_in_packet[j:j+5]))
            msgb += bytes(pixels_in_packet[j:j+5])
        sock.sendto(msgb, (UDP_IP, UDP_PORT))
        #return
        time.sleep(0.05)
    print(len(msg))

def clear():
    msg = []
    for i in range(32):
        for j in range(32):
            msg += bytes([i, j, 0, 0, 0])

    max_pixels_per_packet = 1024//5 +1
    print(
        f'max pixels pp {max_pixels_per_packet} - npackets {len(msg)/max_pixels_per_packet}')
    for i in range(0, len(msg), max_pixels_per_packet):
        #print(f'i={i}')
        msgb = b''

        #print(msg[i:i + max_pixels_per_packet])
        # packet
        pixels_in_packet = msg[i:i + max_pixels_per_packet]
        for j in range(0, len(pixels_in_packet), 5):
            #print(pixels_in_packet[j:j+5],bytes(pixels_in_packet[j:j+5]))
            msgb += bytes(pixels_in_packet[j:j+5])
        sock.sendto(msgb, (UDP_IP, UDP_PORT))
        #return
        time.sleep(0.05)
    print(len(msg))

size = (32, 32)

try:
    print(sys.argv[1])
    im = Image.open(sys.argv[1]).convert('RGB')
    send_image(process_image(im))
except IndexError:
    clear()
#send_image(im)

#send_test()
