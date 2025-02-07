ARG BUILD_FROM
FROM ${BUILD_FROM}

# Copy files
WORKDIR /usr/src/app
COPY run.py .
COPY rootfs /

# Debug: Show init file and permissions
RUN ls -la /init && \
    # Ensure S6 overlay directories exist
    mkdir -p \
        /etc/services.d \
        /etc/cont-init.d \
        /etc/cont-finish.d \
        /etc/fix-attrs.d && \
    # Fix permissions
    chmod +x /init && \
    chmod -R 755 /etc/services.d && \
    chmod -R 755 /etc/cont-init.d && \
    chmod -R 755 /etc/cont-finish.d

# Switch to root for init
USER root

ENTRYPOINT [ "/init" ]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
