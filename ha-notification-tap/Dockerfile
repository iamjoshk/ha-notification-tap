ARG BUILD_FROM
FROM $BUILD_FROM

# Set Python to use UTF-8 encoding
ENV PYTHONIOENCODING=utf-8

WORKDIR /app

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
        py3-async-timeout

# Copy your application
COPY run.py /app/
COPY requirements.txt /app/

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Run script
CMD [ "python3", "run.py" ]
