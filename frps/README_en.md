# frps

Docker image based on ***frps*** service in [fatedier/frp](https://github.com/fatedier/frp) .

[DockerHub](https://hub.docker.com/r/neuzz/frps) | [GitHub](https://github.com/Neuz/Dockerfiles/tree/main/frps)

---

![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/neuzz/frps) ![Docker Pulls](https://img.shields.io/docker/pulls/neuzz/frps) ![Docker Image Version (latest semver)](https://img.shields.io/docker/v/neuzz/frps) 

---

 [中文文档](README.md) | [ENGLISH](README_en.md)

---

## Table of Contents

- [frps](#frps)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Changelog](#changelog)
  - [Maintainers](#maintainers)
  - [Related](#related)
  - [License](#license)

## Usage

- create your config file `frps.ini`, see more [reference](https://gofrp.org/docs/reference/server-configures/).

    for example:
   
    ```
    [common]
    bind_port = 7000
    dashboard_port = 7500
    dashboard_user = admin
    dashboard_pwd = admin
    ```

- start frps

    ```
    docker run -d --name=frps --restart=always \
        -v <YOUR_FRPS_CONFIG_PATH>:/app/frps.ini  \
        -p 7000:7000 \
        -p 7500:7500 \
        -p 10001-10050:10001-10050 \
        neuzz/frps:latest
    ```

## Changelog

- `latest` - latest version
- `Tags` - history version

## Maintainers

- [viacooky](https://github.com/viacooky)

## Related

- [fatedier/frp](https://github.com/fatedier/frp)

## License

[MIT License](../LICENSE) © 2021 Neuz