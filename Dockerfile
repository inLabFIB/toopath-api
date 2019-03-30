FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y binutils libproj-dev gdal-bin

COPY start.sh /start.sh

EXPOSE 8080

CMD ["/start.sh"]
