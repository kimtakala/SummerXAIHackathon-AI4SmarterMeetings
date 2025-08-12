import os
import sys
import subprocess


def extract_mp3(input_path):
    # Ensure input file exists
    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        return

    # Get file name without extension
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.join("data", base_name)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{base_name}.mp3")

    # Use ffmpeg to extract audio as mp3
    cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-vn",  # no video
        "-acodec",
        "libmp3lame",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-ab",
        "192k",
        "-y",  # overwrite
        output_path,
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Extracted MP3 saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Error during extraction:", e.stderr.decode())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mp3-stripping.py <input_file>")
        sys.exit(1)
    extract_mp3(sys.argv[1])
