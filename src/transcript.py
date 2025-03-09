"""
This module provides a stub for transcribing video clips.
Replace the stub with actual speech-to-text integration (e.g., Whisper, Google Speech API, etc.).
"""

def transcribe_video(video_path):
    """
    Transcribe the video at video_path.
    Returns a list of transcript segments.
    Each segment is a dict: { 'sentence': str, 'start': float, 'end': float }
    
    For now, this is a stub that returns a dummy segment.
    """
    # Dummy implementation: Assume the entire clip is one sentence.
    # In practice, implement your speech-to-text and segmentation logic here.
    dummy_segment = {
        "sentence": "This is a dummy transcript.",
        "start": 0,
        "end": 5  # assume a 5-second segment
    }
    return [dummy_segment]
