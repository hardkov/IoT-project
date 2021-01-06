import paho.mqtt.client as mqtt
import json
from threading import Thread

BASE_TOPIC = "zigbee2mqtt/{name}"
def set_topic(name):
    return (BASE_TOPIC + "/set").format(name= name)

def get_topic(name):
    return (BASE_TOPIC + "/get").format(name= name)

def connect():
    cl = mqtt.Client()
    def finalize():
        cl.connect("localhost", 1883, 10)
        cl.loop_forever()
    return cl, finalize

def simulate(state, name):
    def on_connect(client, _u, _a, _rc):
        client.subscribe(set_topic(name))

    def on_message(client, _userdata, msg):
        try:
            contents = json.loads(msg.payload)

            for key, value in contents.items():
                if key in state.keys():
                    state[key] = value

            response = {}
            for key in contents.keys():
                if key in state.keys():
                    response[key] = state[key]
            client.publish(get_topic(name), json.dumps(response))
        except Exception:
            pass

    client, finilize_connection = connect()
    client.on_connect = on_connect
    client.on_message = on_message
    finilize_connection()

