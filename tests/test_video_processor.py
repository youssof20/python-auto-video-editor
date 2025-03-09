import os
import unittest
from moviepy.editor import VideoFileClip
from video_processor import process_clip, merge_clips

class TestVideoProcessor(unittest.TestCase):
    def test_process_clip_invalid_file(self):
        # Test with a non-existent file, expecting a None result or handled error.
        result = process_clip("non_existent_file.mp4")
        self.assertIsNone(result)

    def test_merge_clips_empty_list(self):
        # Merging an empty list should raise an Exception.
        with self.assertRaises(Exception):
            merge_clips([])

if __name__ == "__main__":
    unittest.main()
