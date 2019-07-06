FROM balenalib/rpi-raspbian:buster
MAINTAINER Ryan Aviles <ryan.aviles@gmail.com>


RUN apt-get update && apt-get install -y git python3 python3-pip python3-dev python3-setuptools \
	build-essential libssl-dev libffi-dev i2c-tools libraspberrypi-bin \
    	--no-install-recommends

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN pip3 install --upgrade wheel setuptools

ADD . /rpi_automator
WORKDIR /rpi_automator

RUN pip3 install -r requirements.txt

ADD bin/rpi_automator /usr/local/bin/
ADD etc/rpi_automator /etc/rpi_automator
ENV PYTHONPATH /rpi_automator

ENTRYPOINT [ "python", "/usr/local/bin/rpi_automator"]