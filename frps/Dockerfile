FROM alpine:latest
LABEL maintainer="viacooky@Neuz <viacooky@qq.com>"

ARG Timezone="Asia/Shanghai"
ARG frp_ver="0.37.1"

ENV APP_PATH="/app"
ENV TIMEZONE=${Timezone}
ENV VERSION=${frp_ver}
ENV DOWNLOAD_URL=https://github.com/fatedier/frp/releases/download/v${VERSION}/frp_${VERSION}_linux_amd64.tar.gz

RUN mkdir -p ${APP_PATH}
WORKDIR ${APP_PATH}

RUN apk add --no-cache --update \
    tzdata wget \
    && ln -sf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE} > /etc/timezone" \
    && wget ${DOWNLOAD_URL} --no-check-certificate \
    && tar -zxf frp_${VERSION}_linux_amd64.tar.gz \
    && mv frp_${VERSION}_linux_amd64/frps frps \
    && mv frp_${VERSION}_linux_amd64/frps.ini frps.ini \
    && rm -rf frp_${VERSION}_linux_amd64.tar.gz frp_${VERSION}_linux_amd64 \
    && apk del wget

CMD ["./frps","-c","./frps.ini"]
