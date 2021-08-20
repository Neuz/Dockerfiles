# frps

基于 [fatedier/frp](https://github.com/fatedier/frp) 服务端 frps 的 docker 镜像.

[DockerHub](https://hub.docker.com/r/neuzz/frps) | [GitHub](https://github.com/Neuz/Dockerfiles/tree/main/frps)

---

![GitHub](https://img.shields.io/github/license/neuz/Dockerfiles) ![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/neuzz/frps) ![Docker Pulls](https://img.shields.io/docker/pulls/neuzz/frps) ![Docker Image Version (latest semver)](https://img.shields.io/docker/v/neuzz/frps/latest) 

---

 [中文文档](README.md) | [ENGLISH](README_en.md)

---

## 内容列表

- [frps](#frps)
  - [内容列表](#内容列表)
  - [用法](#用法)
  - [更新日志](#更新日志)
  - [维护人员](#维护人员)
  - [相关](#相关)
  - [许可](#许可)

## 用法

- 创建配置文件`frps.ini`，详见官方[服务端配置说明](https://gofrp.org/docs/reference/server-configures/).
   
    ```
    [common]
    bind_port = 7000
    dashboard_port = 7500
    dashboard_user = admin
    dashboard_pwd = admin
    ```

- 启动frps

    ```
    docker run -d --name=frps --restart=always \
        -v <YOUR_FRPS_CONFIG_PATH>:/app/frps.ini  \
        -p 7000:7000 \
        -p 7500:7500 \
        -p 10001-10050:10001-10050 \
        neuzz/frps:latest
    ```

## 更新日志

- `latest` 为最新版
- `Tags` 为历史版本

## 维护人员

- [viacooky](https://github.com/viacooky)

## 相关

- [fatedier/frp](https://github.com/fatedier/frp)

## 许可

[MIT License](../LICENSE) © 2021 Neuz