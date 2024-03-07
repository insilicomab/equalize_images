FROM python:3.11.6-slim

RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev

WORKDIR /opt

ADD requirements.txt /opt/
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]