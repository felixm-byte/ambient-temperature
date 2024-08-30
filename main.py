from machine import I2C, Pin, SPI
from time import sleep
from pico_i2c_lcd import I2cLcd
from dht import DHT22
 
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

display = max7219.Matrix8x8(spi, ss, 4)

display.brightness(10)
display.fill(0)
scrolling_message = "Happy day!"
#Get the message length
length = len(scrolling_message)

#Calculate number of columns of the message
column = (length * 8)

#Clear the display.
display.fill(0)
display.show()

def set_color(r,g,b):
    red.value(r)
    green.value(g)
    blue.value(b)


while True:
    dht.measure()
    t = dht.temperature()
    h = dht.humidity()
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
    for x in range(32, -column, -1):     
    #Clear the display
        display.fill(0)

        # Write the scrolling text in to frame buffer
        display.text(scrolling_message ,x,0,1)
        
        #Show the display
        display.show()
      
        #Set the Scrolling speed. Here it is 50mS.
        time.sleep(0.05)