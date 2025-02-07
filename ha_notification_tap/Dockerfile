ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install required packages
RUN \
    apk add --no-cache \
        python3

WORKDIR /usr/src/app

# Copy files
COPY run.py .
COPY rootfs /

# No need for S6 setup - it's in the base image
CMD ["/init"]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
