FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/code
COPY d3api /opt/code/d3api
COPY setup.py /opt/code/

RUN mkdir /opt/requirements
WORKDIR /opt/code

ADD ./requirements /opt/requirements
RUN \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /opt/requirements/development.txt --no-cache-dir && \
    python3 -m pip install --no-cache-dir -e . && \
    sed -i "s/MAX_REQUEST_LINE = 8190/MAX_REQUEST_LINE = 32768/" /usr/local//lib/python3.8/site-packages/gunicorn/http/message.py


#    python3 setup.py -v install

EXPOSE 8083

CMD ["gunicorn", "--bind", "0.0.0.0:8083", \
        "--workers", "2", \
        "--timeout", "600", \
        "--limit-request-line", "524288", "d3api.wsgi:app"]
