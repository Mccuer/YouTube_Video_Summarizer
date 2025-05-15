# YouTube to Podcast Generator

A simple tool that turns YouTube videos into podcast-style audio narrations.

## What It Does

- Converts any YouTube video into a single-narrator podcast
- Creates a natural-sounding script from the video's content
- Generates audio you can listen to anywhere
- Uses YouTube transcripts when available and uses Whisper as a fall back when they are not

## Quick Setup

1. Make sure you have Python installed
2. Install required packages:
```bash
pip install gradio pydub edge-tts ollama yt-dlp youtube-transcript-api transformers librosa
```
3. Download Ollama and the Mistral model:
```bash
# First install Ollama from https://ollama.com
ollama pull mistral:7b
```
4. Download FFmpeg. FFmpeg is needed for yt_dlp, which allows us to get the audio from YouTube videos. The source repository can be found [here][1]. For simplicity I downloaded build 7.7.1 from [here][2]
[1]: https://github.com/FFmpeg/FFmpeg
[2]: https://www.gyan.dev/ffmpeg/builds/

## How to Use

1. Run the app:
```bash
python app.py
```

2. Open the web interface from the link that is generated

3. Paste a YouTube URL and click "Submit"

4. Listen to or download your generated podcast

## How It Works

1. Gets the transcript from YouTube (or creates one if not available)
2. Uses a local LLM to rewrite the transcript as a podcast script
3. Converts the script to speech using a natural-sounding voice
4. Delivers an audio file ready for listening

## Customization

You can change the narrator voice by editing the `NARRATOR_VOICE` variable in `app.py`.

## Notes

1. Current output quality is limited by the model being used due to the available memory I have. Using a larger model, or an API for an LLM, will greatly enhance the quality of podcast generated.
2. Whisper generation is very slow, due to the fact that the audio file must be downloaded and then converted to text in 30 second intervals. This is a good proof of concept but not practicle for actual usage