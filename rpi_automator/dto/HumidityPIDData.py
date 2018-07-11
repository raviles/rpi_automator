

class HumidityPIDData:
    """ Captures data from HumidityPIDController """

    def __init__(self, feedback):
        self.feedback = feedback

    def __str__(self):
        return 'feedback={}'.format(self.feedback)
