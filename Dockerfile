From python:3.12

RUN mkdir /usr/src/app

COPY OPCUA_TestServer.py /usr/src/app

COPY requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

CMD ["python", "./OPCUA_TestServer.py"]