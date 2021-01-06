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

thermostat_name = "thermostat"
thermostat_state = {
        "occupied_heating_setpoint": 20,
        "local_temperature": 0,
        "system_mode": "off",
        "running_state": "idle",
        "local_temperature_calibration": 0
}

lamp_name = "lamp"
lamp_state = {
        "state": "OFF",
        "brightness": 0,
        "color_temp": 0,
        "color_xy": {"x": 0, "y":0}
}

curtains_name = "curtains"
curtains_state = {
        "state": "OPEN",
        "position": 100
}

def thermostat_run():
    simulate(thermostat_state, thermostat_name)

def lamp_run():
    simulate(lamp_state, lamp_name)

def curtains_run():
    simulate(curtains_state, curtains_name)


thermostat_thread = Thread(target=thermostat_run)
lamp_thread = Thread(target=lamp_run)
curtains_thread = Thread(target=curtains_run)

thermostat_thread.start()
lamp_thread.start()
curtains_thread.start()

# thermostat_thread.join()
# lamp_thread.join()
# curtains_thread.join()

