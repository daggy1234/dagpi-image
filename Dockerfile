FROM alpine:edge

COPY prod.requirements.txt .

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk add --no-cache python3 python3-dev py3-pip py3-wheel py3-gunicorn py3-setuptools py3-numpy-dev py3-pillow py3-scipy py3-matplotlib \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install https://ftp.travitia.xyz/uvloop-0.15.0.dev0-cp38-cp38-linux_x86_64.whl \
    && pip install https://ftp.travitia.xyz/scikit_image-0.18.dev0-cp38-cp38-linux_x86_64.whl \
    && pip install --no-cache-dir uvicorn fastapi PyWavelets \
    && apk del .build-deps \
    && apk add --no-cache gcc  curl tar file imagemagick g++ libstdc++ bash

RUN pip install --no-cache-dir -r prod.requirements.txt \
    && adduser -S app \
    && rm prod.requirements.txt

ENV MAGICK_HOME=/usr

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app
WORKDIR /
ENV PYTHONPATH=/app


EXPOSE 5000

RUN ls

CMD ["/start.sh"]