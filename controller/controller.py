from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
import time
import json
from devices.thermostat import ThermostatController
from devices.lamp import LampController
from devices.curtains import CurtainsController

# devices
thermostat = ThermostatController("thermostat")
lamp = LampController('lamp')
curtains = CurtainsController("curtains")

def set_thermostat(state):
    thermostat.occupied_heating_setpoint = state["occupied_heating_setpoint"]
    thermostat.local_temperature = state["local_temperature"]
    thermostat.system_mode = state["system_mode"]
    thermostat.running_state = state["running_state"]
    thermostat.local_temperature_calibration = state["local_temperature_calibration"]

def get_thermostat():
    state = {}

    state["occupied_heating_setpoint"] = thermostat.occupied_heating_setpoint
    state["local_temperature"] = thermostat.local_temperature
    state["system_mode"] = thermostat.system_mode
    state["running_state"] = thermostat.running_state
    state["local_temperature_calibration"] = thermostat.local_temperature_calibration 

    return state

def set_lamp(state):
    lamp.state = state["state"]
    lamp.brightness = state["brightness"]
    lamp.color_temp = state["color_temp"]
    lamp.color_xy = state["color_xy"]

def get_lamp():
    state = {}

    state["state"] = lamp.state
    state["brightness"] = lamp.brightness
    state["color_temp"] = lamp.color_temp
    state["color_xy"] = lamp.color_xy

    return state

def set_curtains(state):
    curtains.state = state["state"]
    curtains.position = state["position"]

def get_curtains():
    state = {}

    state["state"] = curtains.state
    state["position"] = curtains.position

    return state

def subscribe_callback(client, userdata, message):
    message_dict = json.loads(message.payload)

    thermostat_state = message_dict['thermostat']
    lamp_state =  message_dict['lamp']
    curtains_state = message_dict['curtains']

    set_thermostat(thermostat_state)
    set_lamp(lamp_state)
    set_curtains(curtains_state)


# AWS config
clientId = "theme-controller"
rootCAPath = "config/root-CA.crt"
privateKeyPath = "config/theme-controller.private.key"
certificatePath = "config/theme-controller.cert.pem"
host = "a3w259c8e2kscd-ats.iot.us-east-1.amazonaws.com"
port = 8883
subscribe_topic = "theme/actuators/desired"
publish_topic = "theme/sensors/reported"   

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

def mqtt_publish(topic, msg, count = 0):
    if count < 3: 
        try:
            myAWSIoTMQTTClient.publish(topic, msg, 1)
        except publishTimeoutException as e:
            count += 1
            mqtt_publish(topic, msg, count)
    else:
        myAWSIoTMQTTClient.publish(topic, msg, 1)

while True: 
    message = {}
    message['thermostat'] = get_thermostat()
    message['lamp'] = get_lamp()
    message['curtains'] = get_curtains()
    messageJson = json.dumps(message)

    # myAWSIoTMQTTClient.publish(publish_topic, messageJson, 1)
    mqtt_publish(publish_topic, messageJson)
    
    time.sleep(3)
