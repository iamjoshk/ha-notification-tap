ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install python and dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-aiohttp

WORKDIR /usr/src/app

# Copy application files
COPY run.py .

# Run directly without S6
CMD ["python3", "run.py"]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
