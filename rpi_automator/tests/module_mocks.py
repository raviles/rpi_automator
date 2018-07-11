""" These modules are not usually installed when running tests, and their usage will be mocked or stubbed anyways """
import sys
from mock import MagicMock
sys.modules['picamera'] = MagicMock()
sys.modules['picamera.PiCamera'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['Adafruit_DHT'] = MagicMock()
sys.modules['RPi'] = MagicMock()
sys.modules['boto3'] = MagicMock()
