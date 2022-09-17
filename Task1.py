import time
import paho.mqtt.client as paho
import numpy as np
import threading
import keyboard
import os
class mqtt_server:
    def __init__(self, broker = 'pldindustries.com', port = 1883, topic = '/group13x', client_id = 'Group_13', username = 'app_client', password = 'app@1234', break_condition = 0):
        # Server information
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.username = username
        self.password = password
        self.break_condition = break_condition
        # configure mqtt client
        self.client = paho.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)
        print("connecting to broker ", self.broker)
        self.client.connect(self.broker, keepalive=60) #connect

    def change_break_condition(self):
        while(True):
            if keyboard.is_pressed('q'):
                self.break_condition = 1
                return

    def thread_function(self, Inizialization_val, lower_val, upper_val, name, seed, sub_topic, dealay): #Fuction for randomly genarate a sensor value and public thos value within 10s dealay
        rng = np.random.default_rng(seed)
        sensor_previous_val = Inizialization_val #Inizialization sensor previous value
        sensor_topic = self.topic + sub_topic #Get the topic
        while(True):
            #Calculate virtual sensor value with randomly
            rand_num = rng.integers(low=lower_val, high=upper_val, size=1)
            sensor_val = 0.8*sensor_previous_val + 0.2*rand_num[0]
            sensor_val = round(sensor_val, 2)
            if (sensor_val<lower_val):
                sensor_val = lower_val
            if (sensor_val>upper_val):
                sensor_val = upper_val
            print("Publishing {} value: {}".format(name, sensor_val))
            self.client.publish(sensor_topic, sensor_val, qos = 0) # Public
            sensor_previous_val = sensor_val #assigning sensor value for sensor previous value
            if self.break_condition == 1:
                break
            time.sleep(dealay)
            
        self.client.disconnect() #disconnect
            
if __name__ == "__main__":
    os.system("start \"\" http://192.168.8.189:1880/ui/")
    server = mqtt_server()
    break_loop = threading.Thread(target=server.change_break_condition, args=())
    Gas = threading.Thread(target=server.thread_function, args=(35,30,40, 'Gas Sensors', 1, "/Gas01", 10))
    Smoke = threading.Thread(target=server.thread_function, args=(35,30,40,'Smoke Status', 2, "/Smoke01", 10))
    Security = threading.Thread(target=server.thread_function, args=(35,30,40,'Security System Status', 3, "/Security01", 10))
    Temperature = threading.Thread(target=server.thread_function, args=(35,30,40,'Temperature sensor', 4, "/Temperature01", 10))
    Humidity = threading.Thread(target=server.thread_function, args=(35,30,40,'Humidity sensor', 5, "/Humidity01", 10 ))
    Motion = threading.Thread(target=server.thread_function, args=(35,30,40,'Motion Sensors', 6, "/Motion01", 10 ))
    Power = threading.Thread(target=server.thread_function, args=(35,30,40,'Power consumption', 7, "/Power01", 10))
    break_loop.start()
    Gas.start()
    Smoke.start()
    Security.start()
    Temperature.start()
    Humidity.start()
    Motion.start()
    Power.start()