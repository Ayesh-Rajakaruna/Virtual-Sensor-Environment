import time
import paho.mqtt.client as paho
import numpy as np
import threading
#import keyboard
#import os
import json
class mqtt_server:
    def __init__(self, broker = 'pldindustries.com', port = 1883, topic = '/group13x', client_id = 'Group_13', username = 'app_client', password = 'app@1234'):
        # Server information
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.username = username
        self.password = password
        #self.break_condition = 0
        # configure mqtt client
        self.client = paho.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)
        print("connecting to broker ", self.broker)
        self.client.connect(self.broker, keepalive=60) #connect
    """
    def change_break_condition(self):
        while(True):
            if keyboard.is_pressed('q'):
                self.break_condition = 1
                return
    """
    def thread_function(self, lower_val, upper_val, name, isbinary, unit, seed, sub_topic, delay): #Fuction for randomly generate a sensor value and public this value within given delay
        rng = np.random.default_rng(seed)
        sensor_previous_val = (lower_val + upper_val)/2 #Inizialization sensor previous value
        sensor_topic = self.topic + sub_topic #Get the topic
        while(True):
            #Calculate virtual sensor value with randomly
            rand_num = rng.integers(low=lower_val, high=upper_val, size=1)
            sensor_val = 0.8*sensor_previous_val + 0.2*rand_num[0]
            sensor_val = round(sensor_val, 2)
            #Check tha value is inside the range
            if (sensor_val<lower_val): 
                sensor_val = lower_val
            elif (sensor_val>upper_val):
                sensor_val = upper_val
            #For binary output map to 0 and 1
            if (isbinary):
                output_val = round(sensor_val)
            else:
                output_val = sensor_val
            #Make output in jason format
            data = {}
            data['lower_sensor_val'] = '{}'.format(lower_val)
            data['current_sensor_val'] = '{}'.format(output_val)
            data['upper_sensor_val'] = '{}'.format(upper_val)
            data['name'] = '{}'.format(name)
            data['unit'] = '{}'.format(unit)
            json_data = json.dumps(data)
            # Public json_data for mqtt server
            print("Publishing {} value: {}".format(name, output_val))
            self.client.publish(sensor_topic, json_data, qos = 0)
            #Assigning sensor value for sensor previous value 
            sensor_previous_val = sensor_val
            """
            #Apply break condition for this loop (if user put q button in keyboard the loop will be stop) 
            if self.break_condition == 1:
                break
            """
            time.sleep(delay) 
        self.client.disconnect() #disconnect           
if __name__ == "__main__":
    #os.system("start \"\" http://<Enter your Raspberrypi ip>/ui/")
    server = mqtt_server()
    #break_loop = threading.Thread(target=server.change_break_condition, args=())
    Gas01 = threading.Thread(target=server.thread_function, args=(300, 10000, 'MQ-2 Gas sensor', False, 'ppm', 1, "/Gas01", 10))
    Gas02 = threading.Thread(target=server.thread_function, args=(200, 10000, 'MQ-6 Gas sensor', False, 'ppm', 2, "/Gas02", 10))
    Smoke01 = threading.Thread(target=server.thread_function, args=(0.0, 999.9, 'NOVA PM Smoke Sensor SDS011', False, 'μg/m3', 3, "/Smoke01", 10))
    Security01 = threading.Thread(target=server.thread_function, args=(0, 1, 'MC38 Security Sensor', True, 'No unit', 4, "/Security01", 10))
    Temperature01 = threading.Thread(target=server.thread_function, args=(-55, 125, 'DS18B20 - Temperature sensor', False, 'Celsius', 5, "/Temperature01", 10))
    Temperature02 = threading.Thread(target=server.thread_function, args=(-40, 150, 'TMP36 - Temperature sensor', False, 'Celsius', 6, "/Temperature02", 10))
    Humidity01 = threading.Thread(target=server.thread_function, args=(0, 100, 'HS 1101LF Humidity sensor', False, '%RH', 7, "/Humidity01", 10))
    Humidity02 = threading.Thread(target=server.thread_function, args=(0, 100, 'HM 1500LF Humidity sensor', False, '%RH', 8, "/Humidity02", 10))
    Motion01 = threading.Thread(target=server.thread_function, args=(0, 1, 'HC - SR501 PIR motion sensor', True, 'No unit', 9, "/Motion01", 10))
    Power01 = threading.Thread(target=server.thread_function, args=(-60, 20, 'Boonton RTP4118 Power sensor', False, 'dBm', 10, "/Power01", 10))
    #break_loop.start()
    Gas01.start()
    Gas02.start()
    Smoke01.start()
    Security01.start()
    Temperature01.start()
    Temperature02.start()
    Humidity01.start()
    Humidity02.start()
    Motion01.start()
    Power01.start()