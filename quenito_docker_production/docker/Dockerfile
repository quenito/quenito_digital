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

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome as default browser
RUN update-alternatives --install /usr/bin/x-www-browser x-www-browser /usr/bin/google-chrome-stable 200 && \
    update-alternatives --install /usr/bin/gnome-www-browser gnome-www-browser /usr/bin/google-chrome-stable 200 && \
    update-alternatives --set x-www-browser /usr/bin/google-chrome-stable && \
    update-alternatives --set gnome-www-browser /usr/bin/google-chrome-stable

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

