FROM python:3.9-alpine
LABEL maintainer="viacooky@Neuz <viacooky@qq.com>"

ARG Timezone="Asia/Shanghai"

ENV APP_PATH="/app"
ENV TIMEZONE=${Timezone}

RUN mkdir -p ${APP_PATH}
WORKDIR ${APP_PATH}
COPY app ${APP_PATH}

RUN apk add --no-cache --update \
    tzdata \
    && ln -sf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone \
    && pip3 install -r requirements.txt \
    && apk del tzdata

CMD ["python","app.py"]
