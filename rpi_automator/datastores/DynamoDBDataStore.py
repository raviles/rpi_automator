from rpi_automator.datastores.DataStore import DataStore
import boto3
import logging
import time
logger = logging.getLogger()


class DynamoDBDataStore(DataStore):
    """ Assumes AWS credentials are set via environment variable, local configuration, or iam policy """

    def __init__(self, table=None, endpoint_url=None, region='us-east-1', type=None):
        assert table

        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=region,
                                       endpoint_url=endpoint_url)

        self.table = self.dynamodb.Table(table)

    def update(self, module_result):

        if not module_result:
            return

        data = {
            'created': module_result.timestamp.isoformat(),
            'module_name': module_result.module.name
        }
        if module_result.data:
            data.update(vars(module_result.data))

        updates = {k: {'Action': 'PUT', 'Value': v} for k, v in data.items()}
        epoch = int(time.mktime(module_result.timestamp.timetuple()))

        key = {'module_type': module_result.module.__class__.__name__, 'epoch': epoch}

        self.table.update_item(Key=key, AttributeUpdates=updates)

