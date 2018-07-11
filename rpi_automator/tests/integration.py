from __future__ import print_function
from mock import MagicMock
import unittest
import time
import sys

sys.modules['RPi'] = MagicMock()

from apscheduler.schedulers.background import BackgroundScheduler
from modules.BaseModule import BaseModule
from modules.DynamoDBDataSource import DynamoDBDataSource
from modules.RelaySwitch import RelaySwitch



class Validate(unittest.TestCase):

    def setUp(self):
        BaseModule.scheduler = BackgroundScheduler()

    def test(self):

        relay = RelaySwitch({'name': 'light', 'pin': 18, 'value': 1, 'value_toggle': 0, 'duration': 2})
        ddb = DynamoDBDataSource({'name': 'ddbevents', 'table': 'staging-test1-events', 'region': 'us-east-1'})
        ddb.subscribe_to(('light',))

        BaseModule.scheduler.start()
        relay.dispatch()
        time.sleep(4)