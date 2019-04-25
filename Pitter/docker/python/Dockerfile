FROM python:3.6


COPY ./src src
WORKDIR /src

RUN pip3 install -r requirements.txt
COPY ./docker/python/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]