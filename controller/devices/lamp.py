import paho.mqtt.client as mqtt
import json

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

class LampController(object):
    def __init__(self, name):
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

        self.data = {
                'state': "OFF",
                'brightness': 0,
                'color_temp': 0,
                'color_xy': {'x': 0, 'y':0}
        }
        self.name = name

        self.client, finalize_connection = connect()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        finalize_connection()

    @property
    def brightness(self):
        return self.data['brightness']

    @property
    def state(self):
        return self.data['state']

    @property
    def color_temp(self):
        return self.data['color_temp']

    @property
    def color_xy(self):
        return self.data['color_xy']

    def update(self, payload):
        self.client.publish(set_topic(self.name), json.dumps(payload))

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
