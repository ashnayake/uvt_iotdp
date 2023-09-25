import network
import machine

wlan=network.WLAN(network.STA_IF)
try:
    print('ESP_32 WiFi program')
    wlan.active(True)
    ssid='ahalakanda_1'
    psk='ak5981175'
    wlan.connect(ssid,psk)
    while not wlan.isconnected():
        machine.idle()
    print(wlan.ifconfig())
except KeyboardInterrupt:
    print('program exit with CTRL+C')
finally:
    print('exit program')
    wlan.disconnect()
    