import os
import time
from moviepy.editor import VideoFileClip
import whisper
from datetime import timedelta

def extract_audio_from_video(video_path, audio_output="audio.wav"):
    """
    Extracts audio from the video file and saves it as a .wav file.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"The video file '{video_path}' does not exist.")
    
    print(f"Extracting audio from '{video_path}'...")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_output, codec='pcm_s16le')
    print(f"Audio extracted and saved as '{audio_output}'")
    return audio_output

def generate_subtitles_whisper(audio_path, output_srt="output.srt"):
    """
    Generates subtitles from audio using Whisper.
    """
    # Load Whisper model (choose a model size based on your system's capability)
    model = whisper.load_model("base")  # You can choose 'tiny', 'small', 'medium', or 'large' models

    print("Transcribing audio using Whisper...")
    result = model.transcribe(audio_path)
    subtitles = []

    # Process each segment in the transcription result
    for i, segment in enumerate(result['segments']):
        start_time = format_timedelta(timedelta(seconds=segment['start']))
        end_time = format_timedelta(timedelta(seconds=segment['end']))
        text = segment['text'].strip()

        subtitles.append({
            "index": i + 1,
            "start_time": start_time,
            "end_time": end_time,
            "text": text,
        })

    # Write subtitles to an .srt file
    write_srt_file(subtitles, output_srt)
    print(f"Subtitle file '{output_srt}' has been created successfully.")

def write_srt_file(subtitles, output_srt):
    """
    Writes subtitle data to an .srt file.
    """
    print(f"Writing subtitles to '{output_srt}'...")
    with open(output_srt, 'w', encoding='utf-8') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{subtitle['start_time']} --> {subtitle['end_time']}\n")
            f.write(f"{subtitle['text']}\n\n")
    print(f"Subtitle file '{output_srt}' has been created successfully.")

def format_timedelta(td):
    """
    Formats timedelta to SRT timestamp format (HH:MM:SS,MS).
    """
    total_seconds = int(td.total_seconds())
    milliseconds = int(td.microseconds / 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

if __name__ == "__main__":
    # Path to the input video
    video_path = "your_file.mp4"  # Replace with your video file path

    # Step 1: Extract audio
    try:
        audio_path = extract_audio_from_video(video_path)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred during audio extraction: {e}")
    else:
        # Step 2: Generate subtitles with Whisper
        generate_subtitles_whisper(audio_path)
