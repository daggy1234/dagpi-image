FROM alpine:edge

COPY prod.requirements.txt .

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk add --no-cache python3 python3-dev py3-pip py3-wheel py3-gunicorn py3-setuptools py3-numpy-dev py3-pillow py3-scipy py3-matplotlib \
    && apk add --no-cache --virtual .build-deps gcc glib libc-dev make  \
    && pip install https://ftp.travitia.xyz/uvloop-0.15.0.dev0-cp38-cp38-linux_x86_64.whl \
    && pip install https://ftp.travitia.xyz/PyWavelets-1.2.0.dev0c306fd6-cp38-cp38-linux_x86_64.whl \
    && pip install https://ftp.travitia.xyz/scikit_image-0.18.dev0-cp38-cp38-linux_x86_64.whl \
    && pip install --no-cache-dir uvicorn fastapi  \
    && apk add --no-cache gcc  curl tar file  g++ libstdc++ bash git glib glib-dev build-base zlib-dev libpng-dev libjpeg-turbo-dev freetype-dev fontconfig-dev perl-dev ghostscript-dev libtool tiff-dev lcms2-dev libwebp-dev libxml2-dev libx11-dev libxext-dev chrpath libheif-dev librsvg-dev freetype fontconfig ghostscript ghostscript-fonts lcms2 graphviz

RUN pip install --no-cache-dir -r prod.requirements.txt \
    && adduser -S app \
    && rm prod.requirements.txt

RUN git clone https://github.com/carlobaldassi/liblqr && \
    cd liblqr && \
    ./configure && \
    make && \
    make install 
    

RUN curl https://codeload.github.com/ImageMagick/ImageMagick/tar.gz/7.0.10-51 | tar -xz && \
    cd ImageMagick-7.0.10-51 && \
    ./configure --with-lqr && \
    make && \
    make install && \
    cd .. && \
    rm -R ImageMagick-7.0.10-51 && \
    cd .. && \
    rm -R liblqr && \
    apk del .build-deps
    
#ENV MAGICK_HOME=/usr

RUN  magick logo: logo.gif

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app
WORKDIR /
ENV PYTHONPATH=/app


EXPOSE 5000

CMD ["/start.sh"]
