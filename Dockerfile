# Use a minimal Python runtime
FROM python:3.11-slim

# Create and activate a venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /code

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app ./app

# Copy and prepare your startup script
COPY boot/docker-run.sh /boot/docker-run.sh
# Strip any Windows CRLF and make it executable
RUN sed -i 's/\r$//' /boot/docker-run.sh \
    && chmod +x /boot/docker-run.sh

# Expose port and use the script as entrypoint
EXPOSE 8000
ENTRYPOINT ["/boot/docker-run.sh"]
