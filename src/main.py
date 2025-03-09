import os
import sys
from tqdm import tqdm  # Importing tqdm for progress bar
from video_processor import process_clip, merge_clips
from utils import log

def get_input_folder():
    """
    Prompt the user for the input folder.
    """
    input_folder = input("Enter the path to the folder containing your video clips: ").strip()
    
    if not os.path.exists(input_folder):
        sys.exit(f"Input folder '{input_folder}' does not exist.")
    
    return input_folder

def get_output_file():
    """
    Prompt the user for the output file path.
    """
    output_file = input("Enter the output file name (e.g., final_video.mp4): ").strip()
    return output_file

def main():
    # Prompt user for input and output paths
    input_folder = get_input_folder()
    output_file = get_output_file()
    
    # Get list of video files ordered by filename
    try:
        files = sorted([
            os.path.join(input_folder, f)
            for f in os.listdir(input_folder)
            if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
        ])
    except Exception as e:
        sys.exit(f"Error reading input folder: {e}")

    if not files:
        sys.exit("No video files found in the input folder.")

    processed_clips = []
    
    # Adding progress bar for processing clips
    for file in tqdm(files, desc="Processing Clips", unit="clip"):
        try:
            print(f"\nProcessing {file}...")
            clip = process_clip(file)
            if clip is not None:
                processed_clips.append(clip)
        except Exception as e:
            log(f"Error processing {file}: {e}")
    
    if not processed_clips:
        sys.exit("No clips processed successfully.")

    try:
        print("\nMerging clips...")
        final_clip = merge_clips(processed_clips)
        print("\nExporting final video...")
        final_clip.write_videofile(output_file, codec="libx264")
        print(f"Final video saved as {output_file}")
    except Exception as e:
        sys.exit(f"Error during merging or exporting: {e}")

if __name__ == "__main__":
    main()
