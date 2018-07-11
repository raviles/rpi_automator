from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.TempAndHumidityData import TempAndHumidityData

import logging
import Adafruit_DHT

logger = logging.getLogger()


class TempHumiditySensor(BaseModule):
    """
        Reads data from an attached DHT22 sensor device using Adafruit drivers.
        Produces an instance of TempAndHumidityData.
        https://www.adafruit.com/product/385

        Configuration Parameters
        ----------
        type : "TempHumiditySensor"
        pin : int
              Pin number
        name : string
              Unique name describing this instance
        use_fahrenheit : boolean
                        Output fahrenheit instead of celsius. Optional.
        enabled : boolean
                  Enalbed for scheduling, or not. Optional.
        subscribed_to : array
                        A list of module names to read results from. Optional.
        cron : string
               cron-style syntax. Optional.
    """

    def __init__(self, pin=None, use_fahrenheit=False, **kwargs):
        BaseModule.__init__(self, **kwargs)
        self.pin = pin
        self.fahrenheit = use_fahrenheit

    def get_humidity_and_temperature(self):
        return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin)

    def run(self, module_result):
        
        (humidity, temperature) = self.get_humidity_and_temperature()
        if humidity is None or temperature is None:
            logger.error("No data read from sensor")
            return ModuleResult(self)

        temperature = self.__tofahrenheit(temperature) if self.fahrenheit else temperature
        return ModuleResult(self, TempAndHumidityData(temperature, humidity))

    def __tofahrenheit(self, celsius):
        return int(celsius * 9/5.0 + 32)
