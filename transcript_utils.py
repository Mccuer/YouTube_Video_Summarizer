import os
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa

def download_youtube_audio(video_url, output_path="downloaded_audio"):
    filename = f"{output_path}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return filename

def transcribe_audio_with_whisper(audio_path):
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

    audio, sr = librosa.load(audio_path, sr=16000)
    chunk_length = 30 * sr
    overlap = 2 * sr

    all_transcriptions = []
    i = 0
    while i < len(audio):
        end = min(i + chunk_length, len(audio))
        chunk = audio[i:end]
        input_features = processor(chunk, sampling_rate=sr, return_tensors="pt").input_features
        predicted_ids = model.generate(input_features)
        chunk_transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        all_transcriptions.extend(chunk_transcription)
        i = end - overlap if end < len(audio) else len(audio)

    return " ".join(all_transcriptions)

def get_transcript(video_url):
    video_id = video_url.split("v=")[1].split("&")[0]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except:
        print("No captions found. Using Whisper to transcribe audio.")
        audio_path = download_youtube_audio(video_url)
        transcript = transcribe_audio_with_whisper(audio_path)
        os.remove(audio_path)
        return transcript