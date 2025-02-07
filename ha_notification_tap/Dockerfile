ARG BUILD_FROM
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Copy app files
COPY run.py .

# Use S6-Overlay for service management
COPY rootfs /
RUN chmod a+x /etc/services.d/notify-tap/run

CMD [ "/init" ]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
