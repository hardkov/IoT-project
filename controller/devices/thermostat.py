import paho.mqtt.client as mqtt
import json

BASE_TOPIC = "zigbee2mqtt/{name}"

def set_topic(name):
    return (BASE_TOPIC + "/set").format(name=name)


def get_topic(name):
    return (BASE_TOPIC + "/get").format(name=name)


def connect():
    cl = mqtt.Client()
    def finalize():
        cl.connect_async("localhost", 1883, 10)
        cl.loop_start()
    return cl, finalize

class ThermostatController(object):
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
                'occupied_heating_setpoint': 20,
                'local_temperature': 0,
                'system_mode': 'off',
                'running_state': 'idle',
                'local_temperature_calibration': 0
        }
        self.name = name

        self.client, finalize_connection = connect()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        finalize_connection()

    @property
    def occupied_heating_setpoint(self):
        return self.data['occupied_heating_setpoint']

    @property
    def local_temperature(self):
        return self.data['local_temperature']

    @property
    def system_mode(self):
        return self.data['system_mode']

    @property
    def running_state(self):
        return self.data['running_state']

    @property
    def local_temperature_calibration(self):
        return self.data['local_temperature_calibration']

    def update(self, payload):
        self.client.publish(set_topic(self.name), json.dumps(payload))

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