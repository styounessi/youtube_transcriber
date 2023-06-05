FROM python:3.11.3-slim

WORKDIR /youtube_transcriber

COPY requirements.txt .

# Install FFmpeg and other dependencies
RUN apt-get update && apt-get install git -y
RUN pip3 install -r requirements.txt
RUN apt-get install -y ffmpeg

COPY . .

EXPOSE 8080

CMD [ "python3", "app.py" ]
