appFROM python:3.9

WORKDIR /python-docker

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY service/ /service/

WORKDIR /service
EXPOSE 8000
ENTRYPOINT [ "python", "app.py"]