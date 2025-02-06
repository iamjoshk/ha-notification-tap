ARG BUILD_FROM
FROM $BUILD_FROM

# Add env
ENV LANG C.UTF-8

WORKDIR /usr/src/app

# Install requirements for add-on
RUN \
    apk add --no-cache \
        python3 \
        py3-pip

# Copy data
COPY run.py .
COPY requirements.txt .

# Install pip requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy data for add-on
COPY run.py /
RUN chmod a+x /run.py

CMD [ "python3", "/run.py" ]

LABEL \
    io.hass.name="HA Notification Tap" \
    io.hass.description="Handle notification tap actions" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64"
