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

class ThermostatController(object):
    def __init__(self, name):
        self.mqtt, _ = connect()
        self.name = name
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message
        self.state = {}
        self.exposes = ["occupied_heating_setpoint", "local_temperature", "system_mode", "running_state", "local_temperature_calibration"]

        def on_connect(client, userdata, flags, rc):
            self.client = client
            client.subscribe(get_get(name))

        def on_message(_client, _userdata, msg):
            print(msg.payload)
            contents = json.loads(msg.payload)
            print(contents)

            for key, value in contents.items():
                self.state[key] = value

    @property
    def occupied_heating_setpoint(self):
        return self.state['occupied_heating_setpoint']

    @property
    def local_temperature(self):
        return self.state['local_temperature']

    @property
    def system_mode(self):
        return self.state['system_mode']

    @property
    def running_state(self):
        return self.state['running_state']

    @property
    def local_temperature_calibration(self):
        return self.state['local_temperature_calibration']

    def update(self, payload):
        self.client.publish(get_set(self.name), json.dumps(payload))

    def _set(self, key, value):
        payload = {
            key: value
        }
        self.update(payload)

    @occupied_heating_setpoint.setter
    def occupied_heating_setpoint(self, value):
        self._set('occupied_heating_setpoint', value)
    
    @local_temperature.setter
    def brightnlocal_temperatureess(self, value):
        self._set('local_temperature', value)

    @system_mode.setter
    def system_mode(self, value):
        self._set('system_mode', value)

    @running_state.setter
    def running_state(self, value):
        self._set('running_state', value)

    @local_temperature_calibration.setter
    def local_temperature_calibration(self, value):
        self._set('local_temperature_calibration', value)