from machine import I2C, Pin, SPI
from time import sleep
from pico_i2c_lcd import I2cLcd
from dht import DHT22
import random 
import max7219
import network
import socket
import urequests
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

dht = DHT22(Pin(28))

red = machine.Pin(22, machine.Pin.OUT)
blue = machine.Pin(26, machine.Pin.OUT)
green = machine.Pin(27, machine.Pin.OUT)

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

ssid = '(replace with ssd name)'
password = '(replace with p/w)'
city = 'London, UK'
def set_color(r,g,b):
    red.value(r)
    green.value(g)
    blue.value(b)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(3)
    print(wlan.ifconfig())

def get_current_temperature(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = "?latitude={}&longitude={}&current_weather=true".format(latitude, longitude)
    
    response = urequests.get(url + params)
    
    if response.status_code == 200:
        data = response.json()
        current_temperature = data['current_weather']['temperature']
        return current_temperature
    else:
        return None

# for my home city, london
latitude = 51.5074
longitude = -0.1278

options = ["^_^ - I'm finally awake", "Hi!, have a nice day", "Good day, mate!", "Have a great day!", "Have a good one."]
index = 0
try:
    connect()
    lcd.putstr("Internet connected successfully!")
    sleep(5)
    lcd.clear()
except Exception as e:
    lcd.putstr("Failed to connect to network :/".format(ssid))
    sleep(5)
    lcd.clear()
    lcd.putstr("n={}".format(ssid))
    lcd.clear()
    sleep(5)
    lcd.putstr("error={}".format(e))
    sleep(5)
    lcd.clear()

#main loop
lcd.putstr("Loading...")
net_t = get_current_temperature(latitude, longitude)
while True:
    dht.measure()
    t = dht.temperature()
    h = dht.humidity()
    lcd.clear()
    lcd.putstr(options[index])
    sleep(5)
    lcd.clear()
    lcd.putstr("{}oC and {}% humidity".format(t, h))
    sleep(5)
    lcd.clear()
    if net_t != None:
        lcd.putstr("About {}oC outside".format(net_t))
    sleep(5)
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
    