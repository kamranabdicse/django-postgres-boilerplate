# Dockerfile
FROM ubuntu:20.04

# Install Python and Package Libraries
RUN apt-get update --fix-missing && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && DEBIAN_FRONTEND=noninteractive apt-get autoremove && DEBIAN_FRONTEND=noninteractive apt-get autoclean && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    build-essential \
    zlib1g-dev \
    net-tools \
    libpq-dev \
    nginx \
    vim \
    sed \
    curl \
    python3 \
    python3-dev \
    python3-pip \
    pkg-config \
    locales \
    gettext 

ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone  

ARG PROJECT=backend
ARG PROJECT_DIR=/opt/app/${PROJECT}
WORKDIR /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p $PROJECT_DIR
COPY ./$PROJECT/requirements.txt /opt/app/
RUN pip3 install -r requirements.txt

COPY nginx.default /etc/nginx/sites-available/default
COPY timeout.conf /etc/nginx/conf.d/
COPY nginx.core.conf /etc/nginx/nginx.conf
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
 && ln -sf /dev/stderr /var/log/nginx/error.log

COPY $PROJECT /opt/app/$PROJECT
COPY start-server.sh /opt/app/
RUN chown -R www-data:www-data /opt/app

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

EXPOSE 8020
LABEL maintainer="kamranabdicse@gmail.com"
STOPSIGNAL SIGTERM