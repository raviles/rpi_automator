from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.UploadedFileData import UploadedFileData

from datetime import datetime
import boto3
import logging

logger = logging.getLogger()

DEFAULT_S3_BASE = "https://{}.s3.amazonaws.com"


class S3Uploader(BaseModule):
    """
        Accepts a LocalFileData instance and uploads to S3

        Configuration Parameters
        ----------
        type : "S3Uploader"
        bucket_name : string
                      An S3 bucket to send the data to
        base_url : string
                   Hostname to return urls with
        name : string
               Unique name describing this instance
        enabled : boolean
                  Enalbed for scheduling, or not. Optional.
        subscribed_to : array
                        A list of module names to read results from. Optional.
    """

    def __init__(self, bucket_name=None, base_url=None, **kwargs):
        BaseModule.__init__(self, **kwargs)
        self.bucket_name = bucket_name
        self.base_url = base_url if base_url else DEFAULT_S3_BASE.format(bucket_name)
        self.client = boto3.client('s3')

    def run(self, module_result):

        logger.debug("S3Uploader(%s): Uploading %s", self.name, module_result.data.file_path)

        now = datetime.now()
        key = "{}/{}/{}-{}".format(now.strftime("%Y-%m-%d"), module_result.module.name, now.strftime("%s"),
                                   module_result.data.name)
        self.client.upload_file(module_result.data.file_path, self.bucket_name, key)

        url = self.base_url + '/' + self.bucket_name + '/' + key
        return ModuleResult(self, UploadedFileData(module_result.data.name, url))
