from matrix import Matrix
from wifi import connect
import socket

print("Welcome")

m = Matrix()

m.startup_animation()
ip = connect()
m.startup_animation_finish()


def udp():

    port = 1234

    print(ip)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))

    print('waiting....')
    while True:
        data, addr = s.recvfrom(1024)
        #print('received:', data, 'from', addr)
        print(len(data))
        for i in range(0, len(data), 5):
            pixel = data[i:i + 5]
            m[pixel[0], pixel[1]] = [pixel[2], pixel[3], pixel[4]]
        m.write()


udp()
