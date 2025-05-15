import os
import uuid
import asyncio
import gradio as gr
from pydub import AudioSegment
from transcript_utils import get_transcript
import edge_tts
import ollama
import re

# Voice to use for single-perspective narration
NARRATOR_VOICE = "en-US-AriaNeural"

async def synthesize_speech(text, filename, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

def clean_text_for_tts(text):
    text = re.sub(r"#\w+\b", "", text)
    text = re.sub(r"@\w+\b", "", text)
    text = re.sub(r"http\S+|www.\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s([?.!,])", r"\1", text) 
    return text

def generate_narration_script(transcript):
    prompt = f"""
You are a podcast narrator. Based on the transcript below, create a friendly, natural-sounding podcast script (around 5 minutes) using a single narrator voice. Do not format as a conversation and do not mention the user. Instead, write it like a narrative summary, suitable for text-to-speech. Make it engaging and easy to follow. Avoid social media language (no hashtags or handles).

Video Transcript:
\"\"\"{transcript}\"\"\"
"""
    response = ollama.chat(
        model="mistral:7b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

async def create_podcast_from_url(video_url):
    transcript = get_transcript(video_url)
    raw_script = generate_narration_script(transcript)
    cleaned_script = clean_text_for_tts(raw_script)

    temp_filename = f"{uuid.uuid4().hex}.mp3"
    await synthesize_speech(cleaned_script, temp_filename, NARRATOR_VOICE)

    final_audio = AudioSegment.from_file(temp_filename)
    os.remove(temp_filename)

    final_output = f"podcast_{uuid.uuid4().hex}.mp3"
    final_audio.export(final_output, format="mp3")
    return final_output

def generate_podcast(video_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(create_podcast_from_url(video_url))

interface = gr.Interface(
    fn=generate_podcast,
    inputs=gr.Textbox(label="Enter YouTube URL"),
    outputs=gr.Audio(label="Generated Podcast"),
    title="YouTube to Podcast Generator",
    description="Creates a podcast episode from a YouTube video using a natural-sounding narrator voice."
)

if __name__ == "__main__":
    interface.launch()
