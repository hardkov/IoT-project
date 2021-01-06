import paho.mqtt.client as mqtt
import json

BASE_TOPIC = "zigbee2mqtt/{name}"


def get_set(name):
    return (BASE_TOPIC + "/set").format(name=name)


def get_get(name):
    return (BASE_TOPIC + "/get").format(name=name)


def connect():
    cl = mqtt.Client()
    return cl, lambda: cl.connect("localhost")


class curtainsController(object):
    def __init__(self, name):
        def on_connect(client, userdata, flags, rc):
            client.subscribe(get_get(name))

        def on_message(_client, _userdata, msg):
            print(msg.payload)
            contents = json.loads(msg.payload)
            print(contents)

            for key, value in contents.items():
                self.state[key] = value

        self.mqtt, connect1 = connect()
        self.name = name
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message
        self.state = {}
        self.exposes = ['state']



    @property
    def state(self):
        return self.state['state']

    def update(self, payload):
        self.client.publish(get_set(self.name), json.dumps(payload))

    def _set(self, key, value):
        payload = {
            key: value
        }
        self.update(payload)

    @state.setter
    def state(self, value):
        self._set('state', value)
