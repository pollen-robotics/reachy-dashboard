import board
import busio as io
import supervisor
import adafruit_ssd1306

i2c = io.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

#oled.fill(0)

#oled.text('14.0.0.1', 0, 0, 1, size=2)
#oled.show()

while True:
    oled.fill(0)

    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        if not value:
            continue
        ip = value.split('.')
        oled.text(ip[0]+'.'+ip[1]+'.', 0, 0, 1, size=2)
        oled.text(ip[2]+'.'+ip[3], 0, 16, 1, size=2)

    oled.show()
