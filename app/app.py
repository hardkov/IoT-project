from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

current_state = None

def set_romantic_theme():
    current_state['thermostat']["occupied_heating_setpoint"] = 21 
    
    current_state["lamp"]["state"] = "ON"
    current_state["lamp"]["brightness"] = 25 # not bright
    current_state["lamp"]["color_temp"] = 1 # something romantic
    current_state["lamp"]["color_xy"] = {"x": 1, "y": 1} # red color

    current_state["curtains"]["position"] = 0 # closed

def set_comfy_theme():
    current_state['thermostat']["occupied_heating_setpoint"] = 23 
    
    current_state["lamp"]["state"] = "ON"
    current_state["lamp"]["brightness"] = 50 # half-bright
    current_state["lamp"]["color_temp"] = 2 # normal
    current_state["lamp"]["color_xy"] = {"x": 2, "y": 2} # normal

    current_state["curtains"]["position"] = 50 # half-closed

def set_party_theme():
    current_state['thermostat']["occupied_heating_setpoint"] = 19 
    
    current_state["lamp"]["state"] = "ON"
    current_state["lamp"]["brightness"] = 25 # not bright
    current_state["lamp"]["color_temp"] = 3 # fancy
    current_state["lamp"]["color_xy"] = {"x": 3, "y": 3} # fancy

    current_state["curtains"]["position"] = 50 # half-closed

def set_theme(theme_name):
    if theme_name == "romantic":
        set_romantic_theme()
    elif theme_name == "comfy":
        set_comfy_theme()
    elif theme_name == "party":
        set_party_theme()
    else:
        pass

def subscribe_callback(client, userdata, message):
    print(message.payload)

    global current_state

    message_dict = json.loads(message.payload)

    current_state = message_dict

clientId = "theme-application"
rootCAPath = "config/root-CA.crt"
privateKeyPath = "config/theme-application.private.key"
certificatePath = "config/theme-application.cert.pem"
host = "a3w259c8e2kscd-ats.iot.us-east-1.amazonaws.com"
port = 8883

publish_topic = "theme/actuators/desired"
subscribe_topic = "theme/sensors/reported"       

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

while True:
    user_input = input()
    
    if current_state:
        if user_input == "r":
            set_theme("romantic")
        elif user_input == "c":
            set_theme("comfy")
        elif user_input == "p":
            set_theme("party")
        else:
            "Unknown theme"

        messageJson = json.dumps(current_state)
        myAWSIoTMQTTClient.publish(publish_topic, messageJson, 1)
    
    else:
        "Can't set theme now - initial theme is not settled yet"

    time.sleep(3)