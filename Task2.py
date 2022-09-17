import time
import paho.mqtt.client as paho
import numpy as np
import threading

# Server information
broker = 'pldindustries.com'
port = 1883
topic = '/group13x'
client_id = 'Group_13'
username = 'app_client'
password = 'app@1234'

# creating subtopic for Gas sensor 01
Gas_topic = topic + "/Gas01"
# creating subtopic for Smoke sensor 01
Smoke_topic = topic + "/Smoke01"
# creating subtopic for Security System Status 01
Security_topic = topic + "/Security01"
# creating subtopic for Temperature sensor 01
Temperature_topic = topic + "/Temperature01"
# creating subtopic Humidity sensor 01
Humidity_topic = topic + "/Humidity01"
# creating subtopic for Motion Sensors 01
Motion_topic = topic + "/Motion01"
# creating subtopic for Power consumption 01
Power_topic = topic + "/Power01"

def on_message(client, userdata, message): #Way for recevived message
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))

# configure mqtt client
client = paho.Client(client_id)
client.username_pw_set(username, password)
client.on_message = on_message
print("connecting to broker ", broker)
client.connect(broker)

client.loop_start()  # start loop to process received messages
print("subscribing ") # subscribe
client.subscribe(Gas_topic)  
client.subscribe(Smoke_topic)
client.subscribe(Security_topic)
client.subscribe(Temperature_topic)
client.subscribe(Humidity_topic)
client.subscribe(Motion_topic)
client.subscribe(Power_topic)


def thread_function(val, name, seed, sensor_topic): #Fuction for randomly genarate a sensor value and public thos value within 10s dealay
    rng = np.random.default_rng(seed)
    while(True):
        rand_num = rng.integers(low=0, high=10, size=1)
        val = val + 0.1*rand_num[0]
        val = round(val, 2)
        print("publishing {} value: {}".format(name, val))
        client.publish(sensor_topic, val) # Public
        time.sleep(10)
    client.loop_stop() # start loop to process received messages
    client.disconnect() #Disconnect


if __name__ == "__main__":
    Gas = threading.Thread(target=thread_function, args=(30, 'Gas Sensors', 1, Gas_topic))
    Smoke = threading.Thread(target=thread_function, args=(35, 'Smoke Status', 2, Smoke_topic))
    Security = threading.Thread(target=thread_function, args=(40, 'Security System Status', 3, Security_topic))
    Temperature = threading.Thread(target=thread_function, args=(40, 'Temperature sensor', 4, Temperature_topic))
    Humidity = threading.Thread(target=thread_function, args=(35, 'Humidity sensor', 5, Humidity_topic ))
    Motion = threading.Thread(target=thread_function, args=(40, 'Motion Sensors', 6, Motion_topic ))
    Power = threading.Thread(target=thread_function, args=(40, 'Power consumption', 7, Motion_topic))

    Gas.start()
    Smoke.start()
    Security.start()
    Temperature.start()
    Humidity.start()
    Motion.start()
    Power.start()
