from rpi_automator.datastores.DataStore import DataStore
from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.util.ModuleUtils import load_module

import logging
import json
import atexit
from apscheduler.schedulers.background import BlockingScheduler

try:
    from RPi import GPIO
except ImportError:
    GPIO = None

logger = logging.getLogger()

DEFAULT_MODULES_PATH = 'rpi_automator/modules'


def exit_gracefully():
    if GPIO:
        GPIO.cleanup()

atexit.register(exit_gracefully)


class EventDispatcher:

    def __init__(self):
        self.modules = {}

    def init_from_config(self, configuration):

        BaseModule.scheduler = BlockingScheduler()

        if 'datastore' in configuration:
            BaseModule.datastore = DataStore.load(configuration['datastore'])

        self.modules = {}

        for config in configuration['modules']:

            name = config['name']
            module_type = config['type']

            if config['enabled'] is False:
                logger.info("%s is not enabled.  Skipping.", name)
                continue

            logging.debug("Loading %s", module_type)
            module = load_module(module_type, config, DEFAULT_MODULES_PATH, BaseModule)
            self.modules[name] = module

    def init_from_filename(self, config_filename):
        configuration = self.load_configuration(config_filename)
        self.init_from_config(configuration)

    def run(self, module_name):
        try:
            self.modules[module_name].dispatch()
        except Exception as e:
            logger.error(e, exc_info=True)

    def start(self):
        logger.debug("Running...")
        BaseModule.start()  # blocking

    @staticmethod
    def load_configuration(filename):
        with open(filename, 'r') as f:
            return json.load(f)
