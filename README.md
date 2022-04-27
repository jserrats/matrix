# Matrix

This project contains two folders:

- **esp32** contains the micropython code to be uploaded to an ESP32 (prreviously flashed with an interpter)
- **sender** contains a script to perform image processing and send images to the esp32

## Upload files to ESP32

```
ampy -p /dev/ttyUSB0 ls
ampy -p /dev/ttyUSB0 put esp32/
```

## Send images to ESP32

Tested with jpg, jpeg, png and webp.

```
python3 send_udp.py test.png
```