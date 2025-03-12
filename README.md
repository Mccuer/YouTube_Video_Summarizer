# YouTube Video Summarization Tool
This tool provides functionality to generate transcripts from YouTube videos using either available captions or automatic speech recognition via Whisper.

## Overview

This project is part 1 of a larger YouTube video summarization tool. The current implementation focuses on the transcription aspect, with more features coming soon.

## Features

* Download audio from YouTube videos
* Attempt to fetch existing captions from YouTube videos
* Fall back to Whisper speech-to-text transcription when captions are unavailable
* Process longer audio files by chunking them into manageable segments
* Clean up temporary audio files automatically

## Installation

Prerequisites
* Python 3.7+
* FFmpeg 

FFmpeg is needed for yt_dlp, which allows us to get the audio from YouTube videos. The source repository can be found [here][1]. For simplicity I downloaded build 7.7.1 from [here][2]
[1]: https://github.com/FFmpeg/FFmpeg
[2]: https://www.gyan.dev/ffmpeg/builds/

## Dependencies

Dependencies can be found in the requirements.txt file, or can be installed using the following command:

~~~
pip install yt-dlp youtube-transcript-api transformers torch librosa
~~~

## Usage

Basic usage is as follows:

~~~~
from transcription_generator import generate_transcript

# Generate transcript for a YouTube video
video_url = "https://www.youtube.com/watch?v=I0-izyq6q5s"
transcript = generate_transcript(video_url)
print(transcript)
~~~~

If you prefer to always use Whisper for transcription (even when YouTube captions are available), you can make the following change:

~~~~
from transcription_generator_whisper_only import generate_transcript

# Generate transcript for a YouTube video
video_url = "https://www.youtube.com/watch?v=I0-izyq6q5s"
transcript = generate_transcript(video_url)
print(transcript)
~~~~

Please note whisper only mode takes much longer than checking for transcripts, but it is a useful fallback when captions are not available. Using Whisper only can mean that videos take minutes or hours to transcribe but is none the less a fun exercise. Whisper only mode will print chunks as they are transcribed to ensure that it is functioning properly.