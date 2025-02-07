ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install python
RUN apk add --no-cache python3 py3-pip py3-aiohttp

WORKDIR /usr/src/app
COPY run.py .
COPY rootfs /

CMD ["/usr/bin/with-contenv", "python3", "/usr/src/app/run.py"]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
