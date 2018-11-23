## Raspberry Pi Automator

An extendable, event-driven automation tool for Raspberry Pi GPIO components.  

The automator provides a built-in cron facility (via `apscheduler`) and a chainable component model.

##### Installation
```commandline
pip install rpi_automator
```

##### Running
```commandline
rpi_automator --config /<path to your config.json>
```
Will block until SIGTERM is received.

## Usage
The automator can be run in two different ways:

**1) Using code**

```python
cam = PICamera(name='backyard_cam', width=640, height=480, cron="*/15 5-17 * * *")
s3 = S3Uploader(bucket_name='my-house-images', base_url='http://d1w07f3h9z0.cloudfront.net')

cam.then(s3)

button = ButtonDetector(name='red_button', pin=4)
light_relay = RelaySwitch(name='backyard_light', pin=8)

light_relay.then(cam)
button.then(light_relay)

BaseModule.start()
```

The above code will do the following:
> Take a photo and upload to an S3 bucket every 15 minutes from 5am to 5pm each day.

> If the red button is pushed, turn on the light and then take a photo.

    
A `DataStore` implementation can be optionally set to send each module result to a backend storage.  New data stores can be 
    created by sub-classing `DataStore`.
    
```python
BaseModule.datastore = DynamoDBDataStore(table='house_data')
```

See [rpi_automator_web](https://github.com/raviles/rpi_automator_web) for DynamoDB setup and data visualizer.

**2) Using a configuration file**

```javascript
{
  "datastore" : "DynamoDBDataStore",

  "modules" : [
    {
      "type" : "modules/PICamera",
      "name" : "piCam1",
      "cron" : "*/15 * * * *",
      "enabled" : true
    },
    {
      "type" : "modules/S3Uploader",
      "bucket_name" : "my-cam-images",
      "name" : "s3",
      "subscribed_to" : ["piCam1"],
      "enabled" : true
    },
    {
      "type" : "modules/TempHumiditySensor",
      "name" : "temp1",
      "use_fahrenheit" : true,
      "cron" : "*/1 * * * *",
      "enabled" : true
    },
    {
      "type" : "modules/RelaySwitch",
      "name" : "light",
      "cron" : "0 7 * * *",
      "duration": 43200,
      "pin" : 18,
      "value" : 1,
      "enabled" : true
    },
    {
      "type" : "ButtonDetector",
      "name" : "wateringButton1",
      "enabled" : true,
      "pin" : 28
    },
    {
      "type" : "RelaySwitch",
      "name" : "waterPump1",
      "duration": 10,
      "pin" : 20,
      "value" : true,
      "value_toggle" : false,
      "subscribed_to" : ["wateringButton1"],
      "enabled" : true
    }
  ]
}
```
    
The configuration file above will automate the following actions:

>Every 15 minutes, take a photo using the attached camera module and upload to S3.

>Every minute, read from a DHT22 temperature & humidity sensor.

>At 7am each day, enable the attached relay power switch (via pin 18) to turn on a light for 12 hours.

>Run the attached water pump (waterPump1) for 10 seconds when the watering button (wateringButton1) is pressed.

In each case, result data will be sent to DynamoDB

Run via:
    
```commandline
rpi_automator --config /<path to your config.json>
```

## Available Modules

- [PICamera](rpi_automator/modules/PICamera.py): V2 Raspberry PI camera module
- [ButtonDetector](rpi_automator/modules/ButtonDetector.py): Basic push button
- [CV2Camera](rpi_automator/modules/CV2Camera.py): USB-based web cam
- [RelaySwitch](rpi_automator/modules/RelaySwitch.py): Relay switch controlling power to a connected device
- [TempHumiditySensor](rpi_automator/modules/TempHumiditySensor.py): Reads data from a DHT22 temperature/humidity sensor
- [S3Uploader](rpi_automator/modules/S3Uploader.py): Modules that generate files can return LocalFileData and get 
uploaded to an S3 bucket

Multiple instances of each module can be configured for different purposes e.g. several instances of `RelaySwitch`
for different lights, each operating on their own GPIO pin.

## Custom Modules
Create new modules by sub-classing [`modules.BaseModule`](rpi_automator/modules/BaseModule.py). The directory
containing the source code should be added to $PYTHONPATH (or `sys.path`).

Custom datastores can also be created by subclassing [`datastores.DataStore`](rpi_automator.datastores.DataStore.py).

## Running Tests

```commandline
cd rpi_automator
export PYTHONPATH=.
python -m unittest tests.EventControllerTests.EventControllerTests
```
