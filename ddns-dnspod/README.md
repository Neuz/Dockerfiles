```
docker run -dit \
    -e DNSPOD_ID=252919 \
    -e DNSPOD_TOKEN=e81993415df847c189188ec84f20ecaf \
    -e DOMAIN=less.host \
    -e SUB_DOMAIN=aa \
    -e INTERNAL=5 \
    -e EMAIL=viacooky@qq.com \
    neuzz/ddns-dnspod:latest
```

```
docker run -dit \
    -v config.cfg:/ddns.config \
    neuzz/ddns-dnspod:latest
```