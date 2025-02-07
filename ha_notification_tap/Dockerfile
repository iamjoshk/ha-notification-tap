ARG BUILD_FROM
FROM ${BUILD_FROM}

# Copy files
WORKDIR /usr/src/app
COPY run.py .
COPY rootfs /

# Use s6-overlay from base image
ENTRYPOINT [ "/init" ]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
