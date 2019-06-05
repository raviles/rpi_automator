from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.RelaySwitchData import RelaySwitchData

from pyvesync import VeSync
from datetime import datetime
from datetime import timedelta
import os
import sys
import logging

logger = logging.getLogger()



class VeSyncOutlet(BaseModule):

    """
        Module interacting with VeSync-supported (Etekcity) smart outlets (https://smile.amazon.com/s?k=vesync+etekcity). 
        Configuration Parameters
        ----------
        type : "VeSyncOutlet"
        vesync_name: string
                     Name of the device in the VeSync app
        duration : int
                   Duration in seconds, toggles between value and value_toggle. Optional.
        initial_on_off: string
                        First trigger value of 'on' or 'off'
        name : string
               Unique name describing this instance
        enabled : boolean
                  Enabled for scheduling, or not. Optional.
        subscribed_to : array
                        A list of module names to read results from. Optional.
        cron : string
               cron-style syntax. Optional.
    """

    def __init__(self, vesync_name, duration, initial_on_off, **kwargs):
        BaseModule.__init__(self, **kwargs)

        self.vesync_name = vesync_name
        self.duration = duration
        self.next_value = self.value_initial = initial_on_off

        self.manager = VeSync(os.environ['VESYNC_USERNAME'], os.environ['VESYNC_PASSWORD'])
        self.manager.login()
        self.manager.update()

        self.device = next( filter( lambda x:x.device_name==vesync_name, self.manager.outlets), None)
        if self.device is None:
            raise Exception("Unable to find Vesync device " + vesync_name)


    def run(self, module_result):

        current_value = self.next_value
        if self.next_value == 'on':
            self.device.turn_on()
            self.next_value = 'off'
        else:
            self.device.turn_off()
            self.next_value = 'on'

        
        result = ModuleResult(self)
        # if we're set to change values in 'duration' seconds
        if self.next_value != self.value_initial and self.duration:
            duration = int(self.duration) # seconds
            run_at = datetime.now() + timedelta(seconds=duration)

            logger.info("Will toggle at %s", run_at)

            result.data = RelaySwitchData(duration)
            self.schedule_run(run_at, name=self.name + str(current_value), module_result=result)

        # if this run is the result of a previous run and we've reached the toggle state
        if module_result and module_result.module == self and current_value == 'off':
            module_result.data.completion_time = datetime.now().isoformat()
            return module_result
        




        