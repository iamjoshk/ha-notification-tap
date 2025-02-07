ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
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
        s6-utils

# Copy root filesystem
COPY rootfs /

# Set permissions for S6 scripts and configs
RUN chmod a+x /etc/services.d/notify-tap/run \
    && chmod a+x /etc/services.d/notify-tap/finish \
    && chmod 644 /etc/services.d/notify-tap/type \
    && chmod 644 /etc/services.d/notify-tap/notification-fd

WORKDIR /usr/src/app

# Copy application files
COPY run.py .

# Make script executable
RUN chmod a+x run.py

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
