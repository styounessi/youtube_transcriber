FROM python:3.11.4-slim

COPY requirements.txt .

# Install FFmpeg and other dependencies
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

WORKDIR /youtube_transcriber
COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
