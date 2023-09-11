from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import threading
import pymongo #database client package for python

myclient = pymongo.MongoClient("mongodb://localhost:27017/") #establish connection with mongodb database
iotdb=myclient['uvt_iotdp'] #load the database
temp_data=iotdb["temp"] #load the temperature collection
alarm_data=iotdb["alarm"] #load the alarm collection
motor_data=iotdb["motor"] #load the motor collection


ENDPOINT = ""
CLIENT_ID = "app1"
PATH_TO_CERTIFICATE = ""
PATH_TO_PRIVATE_KEY = ""
PATH_TO_AMAZON_ROOT_CA_1 = ""
topic_alarm = "alarm/alarm1"
topic_temp="temp/therm1"
topic_motor="motor/motor1"

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection_app = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))

connect_future_app = mqtt_connection_app.connect()
connect_future_app.result()
print("Connected!")

def pub_motor_speed(speed,time,topic_motor):
    message={"time":time,"speed":speed}
    mqtt_connection_app.publish(topic=topic_motor, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + topic_motor)
    motor_data.insert_one(message)

def pub_alarm_stat(stat,time,topic_alarm):
    message = {"time":time,"status":stat}
    mqtt_connection_app.publish(topic=topic_alarm, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + topic_alarm)
    alarm_data.insert_one(message)
    
def on_message_received_temp(topic, payload, dup, qos, retain):
    data_dict = json.loads(payload.decode('utf-8'))
    t=data_dict['time']
    alarm_state='off'
    if data_dict['temp']>30:
        alarm_state='on'
        pub_motor_speed(1,t,"motor/motor1")
    else:
        pub_motor_speed(0,t,"motor/motor1")
    pub_alarm_stat(alarm_state,t,"alarm/alarm1")
    temp_data.insert_one({"time":t,"temp":data_dict['temp']})
    
#subscribing to a topic therm/temp1
subscribe_future, packet_id = mqtt_connection_app.subscribe(
    topic="temp/therm1",
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received_temp
)

subscribe_result = subscribe_future.result()
print(f'Subscribed to {topic_temp}')

threading.Event().wait()