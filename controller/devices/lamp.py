import paho.mqtt.client as mqtt
import json

BASE_TOPIC = "zigbee2mqtt/{name}"
def get_set(name):
    return (BASE_TOPIC + "/set").format(name= name)

def get_get(name):
    return (BASE_TOPIC + "/get").format(name= name)

def connect():
    cl = mqtt.Client()
    return cl, lambda: cl.connect("localhost")

class LampController(object):
    def __init__(self, name):
        self.client, connect_handle = connect()
        self.name = name
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        connect_handle()
        self.state = {}
        self.exposes = ['state', 'brightness', 'color_temp', 'color_xy']

        def on_connect(client, userdata, flags, rc):
            client.subscribe(get_get(name))

        def on_message(_client, _userdata, msg):
            print(msg.payload)
            contents = json.loads(msg.payload)
            print(contents)

            for key, value in contents.items():
                self.state[key] = value

    @property
    def brightness(self):
        return self.state['brightness']

    @property
    def state(self):
        return self.state['state']

    @property
    def color_temp(self):
        return self.state['color_temp']

    @property
    def color_xy(self):
        return self.state['color_xy']

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
    
    @brightness.setter
    def brightness(self, value):
        self._set('brightness', value)

    @color_temp.setter
    def color_temp(self, value):
        self._set('color_temp', value)

    @color_xy.setter
    def color_xy(self, value):
        self._set('color_xy', value)
