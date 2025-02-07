ARG BUILD_FROM
FROM ${BUILD_FROM}

WORKDIR /app
COPY run.py .

CMD ["python3", "run.py"]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
