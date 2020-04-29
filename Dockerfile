FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y software-properties-common

COPY requirements-ubuntu /usr/src/app/

RUN ./requirements-ubuntu

COPY requirements-pip.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements-pip.txt

COPY record.py /usr/src/app/

CMD [ "python", "./record.py" ]
