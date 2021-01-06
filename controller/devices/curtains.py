from Controller import *

class CurtainsController(Controller):
    def __init__(self, name):
        super().__init__(
            { 'state': "OPEN", 'position': 100 },
            name
        )

    @property
    def state(self):
        return self.state['state']

    @property
    def position(self):
        return self.position['position']

    @state.setter
    def state(self, value):
        self._set('state', value)

    @position.setter
    def position(self, value):
        self._set('position', value)
