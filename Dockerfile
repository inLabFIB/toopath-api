FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y binutils libproj-dev gdal-bin

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

COPY start.sh /start.sh

EXPOSE 8080

CMD ["/start.sh"]
