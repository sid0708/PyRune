FROM registry.petuum.com/dev/base-python36:latest
USER 0
RUN mkdir /code
WORKDIR /code
RUN pip3 install paho-mqtt==1.5.0
RUN pip3 install tenacity
RUN pip3 install pulsar-client==2.10.0
RUN pip3 install pykafka
ADD . /code/
CMD ["python3", "janus_pulsar.py"]