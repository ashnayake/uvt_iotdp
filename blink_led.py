from machine import Pin
import time

try:
    print('ESP32 blink program')
    pin=Pin(21,Pin.OUT) #21gpio pin please check the layout 
    while True:
        pin.on()
        time.sleep_ms(500)#500 microseconds 
        pin.off()
        time.sleep_ms(500)
except KeyboardInterrupt:
    print('program exit with CTRL+C')
finally:
    print('exit program')