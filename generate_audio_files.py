from datasets import load_dataset
import os
import random
import soundfile as sf
import numpy as np

# Login using e.g. `huggingface-cli login` to access this dataset
print("Loading LibriSpeech dataset info...")
# First get dataset info without downloading
ds_info = load_dataset("openslr/librispeech_asr", "clean", split="test", streaming=True)

# LibriSpeech test.clean has about 2620 samples
# Generate 3 random positions
total_samples = 2600  # Approximate size of test.clean split
random_positions = sorted(random.sample(range(total_samples), 3))

print(f"Selected random positions: {random_positions}")

# Variables for folder naming and audio stitching
folder_name = None
all_audio_data = []
all_transcripts = []
sample_rate = None

print("Downloading only 3 specific audio files...")
for i, pos in enumerate(random_positions):
    print(f"Getting sample at position {pos}...")

    # Skip to the random position and take 1 sample
    ds_at_pos = load_dataset(
        "openslr/librispeech_asr", "clean", split="test", streaming=True
    )
    sample = next(iter(ds_at_pos.skip(pos).take(1)))

    # Get audio data
    audio_array = sample["audio"]["array"]
    current_sample_rate = sample["audio"]["sampling_rate"]

    # Set sample rate from first file
    if sample_rate is None:
        sample_rate = current_sample_rate

    # Create filename and folder name from first file
    speaker_id = sample["speaker_id"]
    chapter_id = sample["chapter_id"]
    utterance_id = sample["id"]

    if folder_name is None:
        folder_name = f"{speaker_id}-{chapter_id}-{utterance_id}"[:10]

    filename = f"{speaker_id}-{chapter_id}-{utterance_id}.flac"

    # Store audio data for stitching
    all_audio_data.append(audio_array)
    all_transcripts.append(sample["text"])

    print(f"Collected: {filename}")
    print(f"Transcript: {sample['text'][:50]}...")
    print()

# Create output directory with folder name from first file
output_dir = os.path.join("data", folder_name)
os.makedirs(output_dir, exist_ok=True)

print(f"Saving files to: {output_dir}")

# Save individual files
for i, (audio_data, transcript) in enumerate(zip(all_audio_data, all_transcripts)):
    filename = f"speaker_{i+1}.flac"
    filepath = os.path.join(output_dir, filename)
    sf.write(filepath, audio_data, sample_rate)

    # Save transcript
    transcript_file = os.path.join(output_dir, f"speaker_{i+1}.txt")
    with open(transcript_file, "w") as f:
        f.write(transcript)

    print(f"Saved individual file: {filename}")

# Stitch all audio files together
print("Stitching audio files together...")
combined_audio = np.concatenate(all_audio_data)
combined_filepath = os.path.join(output_dir, f"combined_audio.flac")
sf.write(combined_filepath, combined_audio, sample_rate)

# Save combined transcript
combined_transcript = "\n\n".join(
    [f"[SPEAKER_{i+1}] {transcript}" for i, transcript in enumerate(all_transcripts)]
)
combined_transcript_file = os.path.join(output_dir, f"combined_transcript.txt")
with open(combined_transcript_file, "w") as f:
    f.write(combined_transcript)

print(f"✅ Saved combined audio: combined_audio.flac")
print(f"✅ Total duration: {len(combined_audio) / sample_rate:.2f} seconds")

print(
    f"✅ Successfully saved 3 individual audio files and 1 combined file to {output_dir}"
)
print("Files created:")
print("  - speaker_1.flac, speaker_2.flac, speaker_3.flac (individual)")
print(f"  - combined_audio.flac (stitched together for speaker identification testing)")
print("  - corresponding .txt files with transcripts")
