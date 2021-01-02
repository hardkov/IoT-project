from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

clientId = "theme-application"
rootCAPath = "config/root-CA.crt"
privateKeyPath = "config/theme-application.private.key"
certificatePath = "config/theme-application.cert.pem"
host = "a3w259c8e2kscd-ats.iot.us-east-1.amazonaws.com"
port = 8883

publish_topic = "theme/actuators/desired"
subscribe_topic = "theme/sensors/reported"       

def subscribe_callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.subscribe(subscribe_topic, 1, subscribe_callback)

time.sleep(2)

# Publish to the same topic in a loop forever
print("Starting infinite loop")

loopCount = 0
while True: 
    message = {}
    message['message'] = "I want to change the home theme!"
    message['sequence'] = loopCount * 5
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(publish_topic, messageJson, 1)
    
    loopCount += 1
    time.sleep(1)
