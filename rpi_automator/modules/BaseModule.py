from pydispatch import dispatcher
import logging
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger()


class BaseModule(object):
    """ Base class for all modules expressed via configuration and loaded in the
        subscription chain.
        Classes must implement 'run' and accept and return a ModuleResult.
     """
    scheduler = None
    datastore = None

    def __init__(self, type=None, name=None, cron=None, enabled=True, subscribed_to=[]):

        self.enabled = enabled
        self.type = type

        if type is None:
            self.type = self.__class__.__name__

        self.name = name if name else self.type.lower() + str(self.__hash__())

        if cron:
            self.set_cron(cron)

        self.subscribe_to(tuple(subscribed_to))

    def dispatch(self, module_result=None):
        """ dispatch is called via the subscription chain when producers run and return data.  Also called as the
            entry point for scheduled cron jobs and run_once calls.
        """
        logger.debug("Running %s(%s)...", self.type, self.name)
        module_result = self.run(module_result) # calls derived class's 'run' method

        logger.debug("Done running %s(%s)...", self.type, self.name)
        BaseModule._broadcast(module_result)

        signal = self.name + '-signal'
        dispatcher.send(signal=signal, module_result=module_result)

    def run(self, module_result):
        return None

    def subscribe_to(self, modules):
        """ Subscribe this module to the result of each module name in *args
            Args:
                modules(list): list of modules or string names of modules
        """
        for m in modules:
            if isinstance(m, BaseModule):
                m = m.name
            signal = m + '-signal'
            logger.debug("Subscribing %s to signal %s", self.name, signal)
            dispatcher.connect(self.dispatch, signal=signal, sender=dispatcher.Any)

    def remove_subscription(self, modules):
        """ Remove this module's subscription to each module name in *args
            Args:
                modules(list): list of modules or string names of modules
        """
        for m in modules:
            if isinstance(m, BaseModule):
                m = m.name
            signal = m + '-signal'
            logger.debug("Unsubscribing %s to signal %s", self.name, signal)
            dispatcher.disconnect(self.dispatch, signal=signal, sender=dispatcher.Any)

    def set_cron(self, cron):
        assert BaseModule.scheduler

        BaseModule.scheduler.add_job(self.dispatch,
                                  CronTrigger.from_crontab(cron),
                                  None,
                                  id=self.name,
                                  jitter=4)

    def schedule_run(self, run_at_dt, name=None, module_result=None):
        assert BaseModule.scheduler

        if not name:
            name = self.name

        BaseModule.scheduler.add_job(self.dispatch,
                                     kwargs={'module_result': module_result},
                                     next_run_time=run_at_dt,
                                     id=name)

    def then(self, *modules):
        """ Allows for chaining the result of one module to the next
        """
        for m in modules:
            return m.subscribe_to((self,))

        return self

    @staticmethod
    def _broadcast(module_result):
        if not BaseModule.datastore:
            return

        try:
            BaseModule.datastore.update(module_result)
        except Exception as e:
            logger.error(e, exc_info=True)

    @staticmethod
    def start():
        assert BaseModule.scheduler
        BaseModule.scheduler.start()

    def __str__(self):
        return "{}({})".format(self.type, self.name)

