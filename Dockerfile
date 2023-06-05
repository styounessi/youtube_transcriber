FROM python:3.11.3-slim

WORKDIR /youtube_transcriber

COPY . .

# Install FFmpeg and other dependencies
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD [ "python3", "app.py" ]
