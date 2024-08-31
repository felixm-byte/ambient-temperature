from machine import I2C, Pin, SPI
from time import sleep
from pico_i2c_lcd import I2cLcd
from dht import DHT22
import random 
import max7219
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

dht = DHT22(Pin(28))

red = machine.Pin(22, machine.Pin.OUT)
blue = machine.Pin(26, machine.Pin.OUT)
green = machine.Pin(27, machine.Pin.OUT)

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)


def set_color(r,g,b):
    red.value(r)
    green.value(g)
    blue.value(b)

options = ["^_^ - I'm finally awake", "Hi!, have a nice day", "Good day, mate!", "Have a great day!", "Have a good one."]
index = 0
while True:
    dht.measure()
    t = dht.temperature()
    h = dht.humidity()
    lcd.putstr(options[index])
    sleep(5)
    lcd.clear()
    lcd.putstr("{}oC and {}% humidity".format(t, h))
    sleep(5)        # "Hello world!" text would be displayed for 5 secs
    lcd.clear()
    if t > 25:
        lcd.putstr("That's hot, open a window!")
        set_color(1,0,0)

    elif t < 15:
        lcd.putstr("That's chilly, close a window!")
        set_color(0,0,1)
    else:
        lcd.putstr("Sounds like a nice temperature,")
        set_color(0,1,0)
    sleep(2)
    lcd.clear()
    if (index != len(options) - 1):
        index += 1
    else:
        index = 0
    