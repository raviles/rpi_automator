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
        states: list
                List of states. Default: ["on", "off"]
        name : string
               Unique name describing this instance
        enabled : boolean
                  Enabled for scheduling, or not. Optional.
        subscribed_to : array
                        A list of module names to read results from. Optional.
        cron : string
               cron-style syntax. Optional.
    """

    manager = None

    def __init__(self, vesync_name, duration=None, states=["on", "off"], **kwargs):
        BaseModule.__init__(self, **kwargs)

        self.vesync_name = vesync_name
        self.duration = duration
        self.next_idx = 0
        self.states = states

        if not VeSyncOutlet.manager:
            VeSyncOutlet.manager = VeSync(os.environ['VESYNC_USERNAME'], os.environ['VESYNC_PASSWORD'])
            VeSyncOutlet.manager.login()
            VeSyncOutlet.manager.update()

        self.device = next( filter( lambda x:x.device_name==vesync_name, VeSyncOutlet.manager.outlets), None)
        if self.device is None:
            raise Exception("Unable to find VeSync device " + vesync_name)


    def run(self, module_result):

        current_value = self.states[self.next_idx]
        getattr(self.device, 'turn_' + current_value)()

        self.next_idx = (self.next_idx + 1) % len(self.states) # rotate next_idx around `states`
        next_value = self.states[self.next_idx]
        
        result = ModuleResult(self)
        # if we're set to change values in 'duration' seconds
        if next_value != self.states[0] and self.duration:
            duration = int(self.duration) # seconds
            run_at = datetime.now() + timedelta(seconds=duration)

            logger.info("Will toggle at %s", run_at)

            result.data = RelaySwitchData(duration)
            self.schedule_run(run_at, name=self.name + str(current_value), module_result=result)

        # if this run is the result of a previous run and we've reached the toggle state
        if module_result and module_result.module == self and current_value == 'off':
            module_result.data.completion_time = datetime.now().isoformat()
            return module_result
        




        