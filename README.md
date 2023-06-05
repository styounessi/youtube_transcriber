<h1 align="center">
YouTube Transcriber
<img src="https://i.imgur.com/myLczH4.png">
</h1>

A Dash application that transcribes YouTube URLs via OpenAI's transcription engine. Full transcript can be downloaded as a CSV for future use. 

![Example](https://i.imgur.com/Bjq6LMc.gif)

## Dependencies

Installing the core libraries below should cover all dependencies outside of ffmpeg (see futher below). The `requirements.txt` covers these libraries as well. 

- [Dash](https://pypi.org/project/dash/)
- [Dash Mantine Components](https://pypi.org/project/dash-mantine-components/)
- [Pandas](https://pypi.org/project/pandas/)
- [Pytube](https://pypi.org/project/pytube/)
- [Whisper](https://pypi.org/project/openai-whisper/)

### ffmpeg
Whisper requires the command-line version of ffmpeg (not enough to have python-ffmpeg). It can be installed using various package managers:

Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`

Arch: `sudo pacman -S ffmpeg`

Homebrew: `brew install ffmpeg`

Chocolatey: `choco install ffmpeg`

Scoop: `scoop install ffmpeg`

It can also be downloaded and installed manually: [LINK](https://ffmpeg.org/download.html)

### Docker
The `Dockerfile` in this repo covers all of these dependencies too.
```
RUN apt-get update && apt-get install git -y
RUN pip3 install -r requirements.txt
RUN apt-get install -y ffmpeg
```
