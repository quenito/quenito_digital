FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV MODEL_VERSION=claude-sonnet-4-20250514
ENV API_PROVIDER=anthropic

# Install desktop environment matching demo
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    mutter \
    tint2 \
    python3 python3-pip \
    curl git \
    xdotool scrot imagemagick \
    net-tools netcat \
    wget software-properties-common

# Install Firefox from Mozilla PPA (not snap)
RUN add-apt-repository -y ppa:mozillateam/ppa && \
    echo 'Package: firefox*' > /etc/apt/preferences.d/mozilla-firefox && \
    echo 'Pin: release o=LP-PPA-mozillateam' >> /etc/apt/preferences.d/mozilla-firefox && \
    echo 'Pin-Priority: 1001' >> /etc/apt/preferences.d/mozilla-firefox && \
    apt-get update && \
    apt-get install -y firefox

# Python dependencies
COPY docker/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Setup VNC password
RUN mkdir -p ~/.vnc && \
    x11vnc -storepasswd quenito123 ~/.vnc/passwd

# Copy application files
COPY app/ /app/
COPY docker/start_production.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start_production.sh

# Create necessary directories with proper permissions
RUN mkdir -p /app/consciousness /app/logs && \
    chmod -R 755 /app

WORKDIR /app

EXPOSE 5900 8080

CMD ["/usr/local/bin/start_production.sh"]