import argparse
import os
import sys
from video_processor import process_clip, merge_clips
from utils import log

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process video clips to trim out repeats and merge the best takes."
    )
    parser.add_argument(
        "--input_folder", required=True, help="Path to folder containing numbered video clips."
    )
    parser.add_argument(
        "--output_file", required=True, help="Filename for the final merged video."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Ensure the input folder exists
    if not os.path.exists(args.input_folder):
        sys.exit(f"Input folder '{args.input_folder}' does not exist.")

    # Get list of video files ordered by filename
    try:
        files = sorted([
            os.path.join(args.input_folder, f)
            for f in os.listdir(args.input_folder)
            if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
        ])
    except Exception as e:
        sys.exit(f"Error reading input folder: {e}")

    if not files:
        sys.exit("No video files found in the input folder.")

    processed_clips = []
    for file in files:
        try:
            print(f"Processing {file}...")
            clip = process_clip(file)
            if clip is not None:
                processed_clips.append(clip)
        except Exception as e:
            log(f"Error processing {file}: {e}")
    
    if not processed_clips:
        sys.exit("No clips processed successfully.")

    try:
        final_clip = merge_clips(processed_clips)
        final_clip.write_videofile(args.output_file, codec="libx264")
        print(f"Final video saved as {args.output_file}")
    except Exception as e:
        sys.exit(f"Error during merging or exporting: {e}")

if __name__ == "__main__":
    main()
