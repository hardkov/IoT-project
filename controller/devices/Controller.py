import paho.mqtt.client as mqtt
import json
from .deviceShadowClient import DeviceShadowClient

BASE_TOPIC = "zigbee2mqtt/{name}"
def set_topic(name):
    return (BASE_TOPIC + "/set").format(name= name)

def get_topic(name):
    return (BASE_TOPIC + "/get").format(name= name)

def connect():
    cl = mqtt.Client()
    def finalize():
        cl.connect_async("localhost", 1883, 10)
        cl.loop_start()
    return cl, finalize

class Controller(object):
    def __init__(self, initial_data, name, settable_keys):
        def on_connect(client, userdata, flags, rc):
            self.client.subscribe(get_topic(name))

        def on_message(_client, _userdata, msg):
            try:
                contents = json.loads(msg.payload)

                for key, value in contents.items():
                    if key in self.data.keys():
                        self.data[key] = value

            except Exception:
                print("Exception occured")

        self.data = initial_data
        self.name = name
        self.settable_keys = settable_keys

        self.client, finalize_connection = connect()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        finalize_connection()

        self.deviceShadowClient = DeviceShadowClient(self.name)
        self.getShadow()

    def update(self, payload):
        self.client.publish(set_topic(self.name), json.dumps(payload))

    def _set(self, key, value):
        payload = {
            key: value
        }
        self.update(payload)
        self.updateShadow(payload)

    def set_without_shadow_update(self, key, value):
        payload = {
            key: value
        }
        self.update(payload)

    def updateShadow(self, payload):
        self.deviceShadowClient.updateShadow(json.dumps({ "state": { "reported": payload } }))

    def shadowCallback(self, payload, responseStatus, token):
        if responseStatus == "accepted":
            newData = json.loads(payload)
            newData = newData.get("state")

            if newData == None:
                return

            newData = newData.get("reported")

            if newData == None:
                return
            
            for key in newData.keys():
                if key in self.settable_keys:
                    self.set_without_shadow_update(key, newData[key])

    def getShadow(self):
        self.deviceShadowClient.getShadow(self.shadowCallback)

