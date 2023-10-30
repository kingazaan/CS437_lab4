# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np
import logging
from itertools import cycle

# Log all errors
logging.getLogger("AWSIoTPythonSDK.core").setLevel(logging.DEBUG)



# TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 1
device_end = 10

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Endpoint and Credentials path
endpoint = "a8rkzrb921pii-ats.iot.us-east-2.amazonaws.com"
creds = "certificates/AmazonRootCA1.pem"

#Path to your certificates, modify this
certificate_formatter = "./certificates/test-thing-{}/device_{}.certificate.pem"
key_formatter = "./certificates/test-thing-{}/device_{}.private.pem"

class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint(endpoint, 8883)
        self.client.configureCredentials(creds, key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(5)  # 45 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):
        #TODO4: fill in this function for your publish
        self.client.subscribeAsync("vehicleInfo", 0, ackCallback=self.customSubackCallback)        
        self.client.publishAsync("vehicleInfo", Payload, 0, ackCallback=self.customPubackCallback)



print("Loading vehicle data...")
data = []
for i in range(1, 11):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end + 1):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    try:
        client.client.connect()
    except Exception as e:
        print("Error connecting to AWS IoT Core:", str(e))

    clients.append(client)
 
# Turn data into a list of DataFrames into a list of cycle iterators
for i in range(len(data)):
    data[i] = cycle(data[i].iterrows())

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            index, row = next(data[i])
            payload = json.dumps(dict(row))
            print(payload)
            c.publish(payload)

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)