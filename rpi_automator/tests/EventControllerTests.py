from __future__ import print_function
from mock import MagicMock
import unittest
import time
import os
from pydispatch import dispatcher
import module_mocks

from apscheduler.schedulers.background import BackgroundScheduler
from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.modules.PICamera import PICamera
from rpi_automator.modules.S3Uploader import S3Uploader
from rpi_automator.modules.RelaySwitch import RelaySwitch
from rpi_automator.datastores.DynamoDBDataStore import DynamoDBDataStore
from rpi_automator.EventDispatcher import EventDispatcher


class EventControllerTests(unittest.TestCase):

    def setUp(self):

        self.s3_uploads=[]
        self.ddb_data=[]

        PICamera.capture = MagicMock(return_value='tests/resources/python.png')

        BaseModule.datastore = None

    def testRelayDispatch(self):

        relay = RelaySwitch(name='light', pin=18, value=1, value_toggle=0, duration=2)

        def collect(Key=None, AttributeUpdates=None):
            self.ddb_data.append(AttributeUpdates)

        ddb = DynamoDBDataStore(table='staging-test1-events',region='us-east-1', type='DynamoDBDataStore')
        ddb.table.update_item = MagicMock(side_effect=collect)

        BaseModule.datastore = ddb

        BaseModule.scheduler = BackgroundScheduler()
        BaseModule.start()
        relay.dispatch()
        time.sleep(5)

        self.assertEqual(self.ddb_data[0]['created']['Value'], self.ddb_data[1]['created']['Value'])
        self.assertGreater(len(self.ddb_data[1]['completion_time']['Value']), 1)


    def testDispatch(self):

        def collect(Key=None, AttributeUpdates=None):
            self.ddb_data.append(AttributeUpdates)

        ddb = DynamoDBDataStore(table='staging-test1-events', region='us-east-1')
        ddb.table.update_item = MagicMock(side_effect=collect)

        BaseModule.datastore = ddb

        cam = PICamera(**{'name': 'pi1', 'width': 640, 'height': 480})

        s3 = S3Uploader(bucket_name='events_test', base_url='me.com')
        s3.client.upload_file = MagicMock(side_effect=lambda x, y, z:self.s3_uploads.append(x))
        s3.subscribe_to((cam,))

        s32 = S3Uploader(bucket_name='events_test', base_url='me.com')
        s32.subscribe_to((cam,))

        cam.dispatch()

        self.assertEqual(2, len(self.s3_uploads))
        self.assertEqual(3, len(self.ddb_data))

    def testConfig(self):
        # ensure top-level rpi_automator directory is added to PYTHONPATH if running from ide
        controller = EventDispatcher()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        controller.init_from_filename(dir_path + "/config/test-chain.json")

        self.assertEqual(2, len(controller.modules))

        # TODO assert dispatchers wired correctly

    def testThen(self):

        cam = PICamera(width=640, height=480)
        s3 = S3Uploader(bucket_name='events_test', base_url='me.com')
        cam.then(s3)

        class T(BaseModule):
            pass

        t = T()
        t.run = MagicMock()
        s3.then(t)
        cam.dispatch()

        self.assertTrue(t.run.called)


if __name__ == '__main__':
    unittest.main()


