from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.RelaySwitchData import RelaySwitchData

import logging
from datetime import datetime
from datetime import timedelta
from RPi import GPIO

logger = logging.getLogger()


class RelaySwitch(BaseModule):
    """
        Module interacting with a connected relay board controlling power to a connected device.

        Configuration Parameters
        ----------
        type : "RelaySwitch"
        pin: int
             GPIO pin number
        duration : int
                   Duration in seconds, toggles between value and value_toggle. Optional.
        value : int
                First integer value to send to device.
        value_toggle : int
                Second integer value to send to device. Required if `duration` is set.
        name : string
               Unique name describing this instance
        enabled : boolean
                  Enabled for scheduling, or not. Optional.
        subscribed_to : array
                        A list of module names to read results from. Optional.
        cron : string
               cron-style syntax. Optional.
    """

    def __init__(self, pin=None, value=None, duration=None, value_toggle=None, **kwargs):
        BaseModule.__init__(self, **kwargs)

        self.pin = pin
        self.duration = duration
        self.value_initial = self.current_value = value
        self.value_toggle = value_toggle
        self.send(self.current_value)

    def run(self, module_result):

        self.send(self.current_value)

        logger.debug("RelaySwitch(self.name) is now %s", str(self.current_value))

        previous_value = self.current_value
        self.current_value = not self.current_value

        result = ModuleResult(self)

        # if we're set to change values in 'duration' seconds
        if self.current_value != self.value_initial and self.duration:
            duration = int(self.duration) # seconds
            run_at = datetime.now() + timedelta(seconds=duration)

            logger.info("Will toggle at %s", run_at)

            result.data = RelaySwitchData(duration)
            self.schedule_run(run_at, name=self.name + str(self.current_value), module_result=result)

        # if this run is the result of a previous run and we've reached the toggle state
        if module_result and module_result.module == self and previous_value == self.value_toggle:
            module_result.data.completion_time = datetime.now().isoformat()
            return module_result

        return result

    def send(self, value):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, value)


