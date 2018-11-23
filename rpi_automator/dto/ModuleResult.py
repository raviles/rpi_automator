import datetime


class ModuleResult:
    """ Captures results from each implementor of BaseModule and is transferred to
    	subscribed instances
    """

    def __init__(self, module, data=None):
        self.timestamp = self.getTime()
        self.module = module
        self.data = data

    def getTime(clz):
        return datetime.datetime.now()

