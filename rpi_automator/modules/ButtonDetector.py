from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
import logging
from RPi import GPIO

logger = logging.getLogger()


class ButtonDetector(BaseModule):
    """
        Module interacting with a simple pin-based button to trigger subscribed modules for the event.  Activated
        on falling edge of signal.

        Configuration Parameters
        ----------
        type : "ButtonDetector"
        pin : int
              Pin number
        name : string
               Unique name describing this instance
        enabled : boolean
                  Enabled for scheduling, or not. Optional.
        subscribed_to : array
                        A list of module names to read results from. Optional.

    """

    def __init__(self, pin=None, **kwargs):
        BaseModule.__init__(self, **kwargs)
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, lambda pin: self.dispatch(), bouncetime=1500)

    def run(self, module_result):
        """
        Called when the configured button is pressed. This is a no-op which will dispatch to subscribers
        :param module_result:
        :return ModuleResult:
        """
        return ModuleResult(self)

