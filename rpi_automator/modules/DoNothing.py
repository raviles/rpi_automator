from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult


import logging
logger = logging.getLogger()



class DoNothing(BaseModule):

    def __init__(self, width=None, height=None, **kwargs):
        BaseModule.__init__(self, **kwargs)


    def run(self, module_result):
        return ModuleResult(self)

