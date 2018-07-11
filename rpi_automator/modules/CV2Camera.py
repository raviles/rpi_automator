from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.LocalFileData import LocalFileData

import logging
import tempfile, os
import cv2

logger = logging.getLogger()


class CV2Camera(BaseModule):
    """
        Module interacting with a CV2-supported webcam (most USB webcams)

        Configuration Parameters
        ----------
        type : "CV2Camera"
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

        self.cam = cv2.VideoCapture(0)

        self.cam.set(3, width) # set the Horizontal resolution
        self.cam.set(4, height) # Set the Vertical resolution

    def run(self, module_result):

        file_path = self.capture()
        return ModuleResult(self, LocalFileData(file_path, os.path.basename(file_path)))

    def capture(self):
        s, img = self.cam.read()
        if s is None:
          raise Exception("Unable to read from camera")
        fd, file_path = tempfile.mkstemp(suffix='.jpg')
        cv2.imwrite(file_path, img)
        logger.debug("CV2Camera(%s) wrote photo %s", self.name, file_path)

        return file_path
