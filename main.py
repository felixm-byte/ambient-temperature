from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from dht import DHT22
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

dht = DHT22(Pin(28))


while True:
    dht.measure()
    t = dht.temperature()
    h = dht.humidity()
    lcd.putstr(f"Hi! {t}°C and {h}% humidity")
    sleep(5)        # "Hello world!" text would be displayed for 5 secs
    lcd.clear()
    if t > 25:
        lcd.putstr("That's hot, open a window!")
    elif t < 15:
        lcd.putstr("That's chilly, close a window!")
    else:
        lcd.putstr("Sounds like a nice temp.")

    sleep(2)
    lcd.clear()  