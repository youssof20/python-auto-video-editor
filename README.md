# Video Editor Project

This project is a prototype Python-based tool that processes a folder of video clips recorded with repeated sentences. It is designed to automatically trim out stutters and repeated sentences and merge the best takes into a final, seamless video.

## Features

- **Automatic Processing:** Reads a folder of video clips (numbered sequentially) and processes each clip.
- **Transcription Stub:** Uses a stub for speech-to-text transcription (replace with your preferred engine).
- **Best-Take Detection:** Contains a placeholder for selecting the best version of a repeated sentence.
- **Video Merging:** Uses MoviePy to merge the processed clips into a final video.

## Requirements

- Python 3.7+
- [moviepy](https://zulko.github.io/moviepy/)
- Other dependencies as listed in [requirements.txt](requirements.txt)

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
