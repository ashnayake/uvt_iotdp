import network
import machine
import time
import ujson
from umqtt.simple import MQTTClient
import esp32
import ntptime

#mqtt broker
aws_broker=b""
clientid=''
private_key=''
private_cert=''
sub_topic=''
key=None
cert=None

with open(private_key, 'r') as f:
    key = f.read()
with open(private_cert, 'r') as f:
    cert = f.read()
    
sslp = {"key":key, "cert":cert, "server_side":False}

wlan=network.WLAN(network.STA_IF)
try:
    print('ESP_32 WiFi program')
    wlan.active(True)
    wlan.connect(ssid,psk)#updated from boot.py
    while not wlan.isconnected():
        machine.idle()
    print("connceted to wlan {} with ip:{}".format(ssid,wlan.ifconfig()[0]))
    ntptime.settime()
    
    def callback_sub(topic,msg):
        message=ujson.loads(msg)
        print(message)
        
    print("Begin connection with MQTT Broker :: {}".format(aws_broker))
    mqtt = MQTTClient(client_id=clientid, server=aws_broker,port=8883,keepalive=1200,ssl=True,ssl_params=sslp)
    mqtt.connect()
    print("Connected to MQTT  Broker :: {}".format(aws_broker))
    
    mqtt.set_callback(callback_sub)
    mqtt.subscribe(sub_topic)
    
    while True:
        mqtt.check_msg()

except KeyboardInterrupt:
    print('program exit with CTRL+C')
finally:
    print('exit program')
    wlan.disconnect()
    #machine.reset()
