ARG BUILD_FROM
FROM ${BUILD_FROM}

COPY rootfs /
WORKDIR /usr/src/app

# Install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy app
COPY run.py .

# Labels
LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
