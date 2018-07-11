

class TempAndHumidityData:
    """ Captures temperature and humidity data """

    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return 'temperature={}, humidity={}'.format(self.temperature, self.humidity)
