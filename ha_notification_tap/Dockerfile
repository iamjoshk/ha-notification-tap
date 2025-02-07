ARG BUILD_FROM
FROM $BUILD_FROM

# Add env
ENV LANG C.UTF-8

# Install requirements for add-on
RUN \
    apk add --no-cache \
        python3 \
        py3-pip

WORKDIR /usr/src/app

# Copy data
COPY requirements.txt .
COPY run.py .

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Make script executable
RUN chmod a+x run.py

CMD [ "python3", "run.py" ]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7"
