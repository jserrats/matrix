from os import uname
from sys import implementation
import network
import ubinascii
from secrets import SSID, PASSWORD


print(implementation.name)
print(uname()[3])
print(uname()[4])
print()

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("MAC: " + mac)
print()

def connect():
    print('connect to network...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(dhcp_hostname="matrix")
    if not wlan.isconnected():
        print('...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    
    print()
    print('network config:')
    print("interface's IP/netmask/gw/DNS addresses")
    print(wlan.ifconfig())
    return wlan.ifconfig()[0]
    
