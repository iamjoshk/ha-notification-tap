ARG BUILD_FROM
FROM $BUILD_FROM

# Install required packages
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        py3-aiohttp \
        py3-yarl \
        py3-multidict \
        py3-attrs \
        py3-charset-normalizer \
        py3-async-timeout \
        py3-frozenlist \
        py3-aiosignal \
        py3-typing-extensions

WORKDIR /usr/src/app

# Copy application files
COPY run.py .

# Copy service script
COPY rootfs/etc/services.d/notify-tap/run /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
