from Controller import *

class ThermostatController(Controller):
    def __init__(self, name):
        super().__init__(
            {
                    'occupied_heating_setpoint': 20,
                    'local_temperature': 0,
                    'system_mode': 'off',
                    'running_state': 'idle',
                    'local_temperature_calibration': 0
            },
            name
        )

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
