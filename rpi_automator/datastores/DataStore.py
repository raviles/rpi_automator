from rpi_automator.util.ModuleUtils import load_module
import logging
logger = logging.getLogger()

DEFAULT_DATASTORES_PATH = 'rpi_automator/datastores'


class DataStore(object):

    def update(self, module_result):
        raise NotImplementedError("Not implemented")

    @staticmethod
    def load(config):

        module_name = config['type']
        logging.debug("Loading %s", module_name)
        return load_module(module_name, config, DEFAULT_DATASTORES_PATH, DataStore)
