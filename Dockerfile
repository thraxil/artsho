FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD bootstrap.py /code/
ADD requirements /code/
ADD virtualenv.py /code/
RUN ./bootstrap.py
ADD . /code/

