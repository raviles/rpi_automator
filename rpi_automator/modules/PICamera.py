from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.LocalFileData import LocalFileData

import logging
import tempfile, os
import picamera

logger = logging.getLogger()


class PICamera(BaseModule):
    """
        Module interacting with the V2 Raspberry PI camera module.
        https://www.raspberrypi.org/products/camera-module-v2/

        Configuration Parameters
        ----------
        type : "PICamera"
        width : int
                width of camera output, in pixels
        height : int
                height of camera output, in pixels
        name : string
              Unique name describing this instance
        enabled : boolean
                  Enabled for scheduling, or not. Optional.
        subscribed_to : array
              A list of module names to read results from. Optional.
        cron : string
               cron-style syntax. Optional.

    """

    def __init__(self, width=None, height=None, **kwargs):
        BaseModule.__init__(self, **kwargs)
        self.cam = picamera.PiCamera()
        self.cam.vflip = self.cam.hflip = True
        self.cam.resolution = (width, height)

    def run(self, module_result):
        
        file_path = self.capture()
        return ModuleResult(self, LocalFileData(file_path, os.path.basename(file_path)))

    def capture(self):
        fd, file_path = tempfile.mkstemp(suffix='.jpg')
        with os.fdopen(fd, 'w') as open_file:
            self.cam.capture(open_file, 'jpeg')

        logger.debug("PICamera(%s) wrote photo %s", self.name, file_path)
        return file_path
