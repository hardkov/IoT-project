from Controller import *

class LampController(Controller):
    def __init__(self, name):
        super().__init__(
            {
                    'state': "OFF",
                    'brightness': 0,
                    'color_temp': 0,
                    'color_xy': {'x': 0, 'y':0}
            },
            name
        )

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
