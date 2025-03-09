import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from transcript import transcribe_video
from utils import log
from pydub import AudioSegment
import librosa
import numpy as np

def ask_yes_no(question):
    """
    Helper function to ask yes/no questions in the command line.
    Returns True for 'yes' and False for 'no'.
    """
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def setup_configuration():
    """
    Interactive setup that asks the user which features they want to enable.
    """
    print("Welcome to the interactive setup!")
    
    config = {}

    # Ask if they want to enable transcription
    config["enable_transcription"] = ask_yes_no("Do you want to enable transcription?")
    
    # Ask if they want to enable audio normalization
    config["enable_audio_normalization"] = ask_yes_no("Do you want to enable audio normalization?")
    
    # Ask if they want to enable noise reduction
    config["enable_noise_reduction"] = ask_yes_no("Do you want to enable noise reduction?")
    
    # Ask if they want to use best take selection
    config["use_best_take_selection"] = ask_yes_no("Do you want to use best take selection?")
    
    # Ask if they want to enable fade transitions
    config["enable_fade_transitions"] = ask_yes_no("Do you want to enable fade transitions?")
    
    # Ask for minimum clip length
    while True:
        try:
            min_clip_length = float(input("Enter the minimum clip length (in seconds): ").strip())
            if min_clip_length > 0:
                config["min_clip_length"] = min_clip_length
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Ask for fade duration
    while True:
        try:
            fade_duration = float(input("Enter the fade duration (in seconds): ").strip())
            if fade_duration >= 0:
                config["fade_duration"] = fade_duration
                break
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return config

# Load the user configuration
config = setup_configuration()

def process_clip(video_path, config):
    """
    Process a single video clip based on user-defined configuration.
    """
    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        log(f"Error loading video {video_path}: {e}")
        return None

    # Check for clip length (if it's too short to process)
    if clip.duration < config["min_clip_length"]:
        log(f"Clip {video_path} is too short to process. Skipping.")
        return None

    # Transcribe video if enabled
    transcript_segments = None
    if config["enable_transcription"]:
        try:
            transcript_segments = transcribe_video(video_path)
        except Exception as e:
            log(f"Error transcribing video {video_path}: {e}")

    if transcript_segments is None or not transcript_segments:
        log(f"No transcript found for {video_path}, using full clip.")
        return clip
    
    # Use better logic to select the best take if enabled
    if config["use_best_take_selection"]:
        best_segment = select_best_take(transcript_segments)
        if best_segment:
            start, end = best_segment
            try:
                clip = clip.subclip(start, end)
                log(f"Trimmed {video_path} from {start} to {end}")
            except Exception as e:
                log(f"Error trimming video {video_path}: {e}")
    
    # Process audio if enabled
    if config["enable_audio_normalization"]:
        clip = normalize_audio(clip)
    if config["enable_noise_reduction"]:
        clip = reduce_noise(clip)

    return clip

def normalize_audio(clip):
    """
    Normalize audio volume.
    """
    try:
        audio = clip.audio
        audio_filename = "temp_audio.wav"
        audio.write_audiofile(audio_filename)

        # Normalize audio using pydub
        audio_clip = AudioSegment.from_wav(audio_filename)
        audio_clip = audio_clip - audio_clip.dBFS  # Normalize to 0 dBFS

        # Replace audio with normalized version
        denoised_audio = AudioSegment.from_wav("denoised_audio.wav")
        clip = clip.set_audio(denoised_audio)

        os.remove(audio_filename)
        os.remove("denoised_audio.wav")
    except Exception as e:
        log(f"Error in audio normalization: {e}")
    return clip

def reduce_noise(clip):
    """
    Reduce background noise using librosa.
    """
    try:
        audio_filename = "temp_audio.wav"
        clip.audio.write_audiofile(audio_filename)
        y, sr = librosa.load(audio_filename, sr=None)
        y_denoised = librosa.effects.preemphasis(y)
        librosa.output.write_wav("denoised_audio.wav", y_denoised, sr)

        denoised_audio = AudioFileClip("denoised_audio.wav")
        clip = clip.set_audio(denoised_audio)

        os.remove(audio_filename)
        os.remove("denoised_audio.wav")
    except Exception as e:
        log(f"Error in noise reduction: {e}")
    return clip

def select_best_take(transcript_segments):
    """
    Select the best take based on transcript segments.
    """
    if not transcript_segments:
        return None

    # Here, we simply return the first segment for simplicity.
    # For more advanced behavior, this could be modified.
    best = transcript_segments[0]
    return best.get("start", 0), best.get("end", best.get("start", 0) + 5)

def merge_clips(clips, config):
    """
    Merge video clips with fade transitions if enabled.
    """
    try:
        # Apply fade transitions if enabled
        if config["enable_fade_transitions"]:
            for i in range(len(clips)-1):
                clips[i] = clips[i].fadeout(config["fade_duration"])

        final_clip = concatenate_videoclips(clips, method="compose")
        return final_clip
    except Exception as e:
        log(f"Error merging clips: {e}")
        raise
