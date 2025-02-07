ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set Python to use UTF-8 encoding
ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8

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
        py3-typing-extensions \
        python3-dev \
        gcc \
        musl-dev

WORKDIR /usr/src/app

# Copy application files
COPY run.py .

# Make script executable
RUN chmod a+x run.py

# Copy root filesystem
COPY rootfs /

# Set up S6 service
RUN mkdir -p /etc/services.d/notify-tap && \
    chmod -R 755 /etc/services.d/notify-tap && \
    chmod +x /etc/services.d/notify-tap/run && \
    chmod +x /etc/services.d/notify-tap/finish

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
