#! /bin/bash

###
# Set the value of a specified GPIO pin
# - Usage: pin.sh <pin number> <value>

# Get the value of a specified GPIO pin
# - Usage: pin.sh <pin number>
###

PIN=$1
VALUE=$2

PIN_DIR=/sys/class/gpio/gpio$PIN

# establish the pin in userspace
if [ ! -e $PIN_DIR ]; then
  echo "$PIN" > /sys/class/gpio/export
fi

if [ -z $VALUE ]; then

  cat $PIN_DIR/value

else
  # Sets pin as an output
  echo "out" > $PIN_DIR/direction
  echo "$VALUE" > $PIN_DIR/value

fi