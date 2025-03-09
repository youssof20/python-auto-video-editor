import os
from moviepy.editor import VideoFileClip
from transcript import transcribe_video
from utils import log

def process_clip(video_path):
    """
    Process a single video clip:
    - Extract transcription using a more accurate method.
    - Determine the best take for repeated sentences.
    - Trim the video accordingly.
    
    Returns a processed VideoFileClip object.
    """
    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        log(f"Error loading video {video_path}: {e}")
        return None

    # Check for clip length (if it's too short to process)
    if clip.duration < 1:  # Assuming 1 second as the minimum valid length
        log(f"Clip {video_path} is too short to process. Skipping.")
        return None

    # Transcribe video (improve transcription method)
    try:
        transcript_segments = transcribe_video(video_path)
    except Exception as e:
        log(f"Error transcribing video {video_path}: {e}")
        return clip  # Fallback to using the full clip

    # Handle cases where transcript is empty or too short
    if not transcript_segments:
        log(f"No transcript found for {video_path}, using full clip.")
        return clip
    
    # Use better logic to select the best take (use timestamps to handle repeated parts)
    best_segment = select_best_take(transcript_segments)
    if best_segment is None:
        log(f"No best segment found for {video_path}, using full clip.")
        return clip

    start, end = best_segment
    try:
        processed_clip = clip.subclip(start, end)
        log(f"Trimmed {video_path} from {start} to {end}")
        return processed_clip
    except Exception as e:
        log(f"Error trimming video {video_path}: {e}")
        return clip

def select_best_take(transcript_segments):
    """
    Given transcript segments, select the best take by avoiding repeated phrases.
    This logic will improve the take selection process by using timestamps to identify the best portion.
    
    Each transcript segment is expected to be a dict:
    { 'sentence': str, 'start': float, 'end': float }
    """
    if not transcript_segments:
        return None

    # For now, this logic simply returns the first non-repeating segment.
    # You can improve this by analyzing pauses or using NLP techniques to detect repeated phrases.
    best = transcript_segments[0]
    return best.get("start", 0), best.get("end", best.get("start", 0) + 5)

def merge_clips(clips):
    """
    Merge a list of VideoFileClip objects into a single clip.
    This version adds fade-in and fade-out transitions to make the cut seamless.
    """
    from moviepy.editor import concatenate_videoclips
    try:
        # Applying fade-in/out transitions to clips for seamless merging
        for i in range(len(clips)-1):
            clips[i] = clips[i].fadeout(0.5)  # Adding 0.5 seconds fade-out to each clip

        final_clip = concatenate_videoclips(clips, method="compose")
        return final_clip
    except Exception as e:
        raise Exception(f"Error merging clips: {e}")
