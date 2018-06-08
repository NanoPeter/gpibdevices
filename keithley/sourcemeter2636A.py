from enum import Enum

from .sourcemeter2602A import Sourcemeter2602A


class Sourcemeter2636A(Sourcemeter2602A):
    def __str__(self):
        return 'Sourcemeter 2636A {} {}'.format(self._channel, self._dev.resource_name)




