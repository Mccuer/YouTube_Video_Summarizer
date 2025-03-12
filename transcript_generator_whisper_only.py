import os
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa

def download_youtube_audio(video_url, output_path="audio"):
    """
    Downloads the audio from a YouTube video using yt-dlp.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return f"{output_path}.mp3"

def transcribe_audio_with_whisper(audio_path):
    """
    Transcribes the entire audio file using the Hugging Face Whisper model
    by processing it in chunks.
    """
    # Load the processor and model
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

    # Load the audio file and resample to 16kHz
    audio, sr = librosa.load(audio_path, sr=16000)
    
    # Whisper has a max input length of 30 seconds, chunck the audio to ensure entirety is transcribed
    chunk_length = 30 * sr  
    overlap = 2 * sr  
    
    all_transcriptions = []
    
    # Process audio in chunks
    i = 0
    while i < len(audio):
        end = min(i + chunk_length, len(audio))
        chunk = audio[i:end]
        
        input_features = processor(chunk, sampling_rate=sr, return_tensors="pt").input_features
        
        predicted_ids = model.generate(input_features)
        
        chunk_transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        
        print(chunk_transcription)

        all_transcriptions.extend(chunk_transcription)
        
        i = end - overlap if end < len(audio) else len(audio)
    
    full_transcript = " ".join(all_transcriptions)
    return full_transcript

def get_transcript(video_url):
    """
    Fetches the transcript using  Whisper.
    """
    print("Using Whisper to transcribe audio.")
    audio_path = download_youtube_audio(video_url)
    transcript = transcribe_audio_with_whisper(audio_path)

    os.remove(audio_path)
    
    return transcript

def generate_transcript(video_url):
    """
    Generates a transcript for a YouTube video.
    """
    print("Fetching transcript...")
    transcript = get_transcript(video_url)
    print("Transcript Completed")
    return transcript

if __name__ == "__main__":
    # If running file independently replace youtube video url here
    video_url = "https://www.youtube.com/watch?v=3k89FMJhZ00"

    # Generate transcript
    transcript = generate_transcript(video_url)
    print("Transcript:")
    print(transcript)