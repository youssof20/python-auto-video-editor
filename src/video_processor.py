import os
from moviepy.editor import VideoFileClip
from transcript import transcribe_video
from utils import log

def process_clip(video_path):
    """
    Process a single video clip:
    - Extract transcription using a stub function.
    - Determine the best take for repeated sentences.
    - Trim the video accordingly.
    
    Returns a processed VideoFileClip object.
    """
    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        log(f"Error loading video {video_path}: {e}")
        return None

    # Transcribe video (stub function; replace with actual transcription)
    try:
        transcript_segments = transcribe_video(video_path)
    except Exception as e:
        log(f"Error transcribing video {video_path}: {e}")
        return clip  # Fallback to using the full clip

    # Determine the best segment
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
    Given transcript segments, detect repeated sentences and return a tuple (start, end)
    representing the best take.

    For this prototype, we simply choose the first segment as the 'best take'.
    Replace this with a more advanced algorithm as needed.
    
    Each transcript segment is expected to be a dict:
    { 'sentence': str, 'start': float, 'end': float }
    """
    if not transcript_segments:
        return None

    # Example: simply return the first segment's start and end times
    best = transcript_segments[0]
    return best.get("start", 0), best.get("end", best.get("start", 0) + 5)

def merge_clips(clips):
    """
    Merge a list of VideoFileClip objects into a single clip.
    """
    from moviepy.editor import concatenate_videoclips
    try:
        final_clip = concatenate_videoclips(clips, method="compose")
        return final_clip
    except Exception as e:
        raise Exception(f"Error merging clips: {e}")
