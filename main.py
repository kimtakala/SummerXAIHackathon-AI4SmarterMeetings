import whisperx
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main(audio_file):
    print("[1] Transcribing with WhisperX...")

    # Get HF token from environment (supports both .env and GitHub secrets)
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("Error: HF_TOKEN not found in environment variables")
        print("Please either:")
        print("1. Create a .env file with your personal HF_TOKEN for local development")
        print("2. Set HF_TOKEN as an environment variable")
        print("3. For GitHub Actions, use repository secrets")
        return

    # Set up WhisperX parameters
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    batch_size = 16  # reduce if low on GPU mem
    compute_type = "float32"

    # Load model
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    # Load audio
    audio = whisperx.load_audio(audio_file)

    # Transcribe
    result = model.transcribe(audio, batch_size=batch_size)

    # Align whisper output
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    # Diarization (optional)
    try:
        from pyannote.audio import Pipeline

        diarize_model = Pipeline.from_pretrained(
            "pyannote/speaker-diarization", use_auth_token=hf_token
        )
        diarize_model.to(torch.device(device))
        diarize_segments = diarize_model(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result)
        print("✅ Speaker diarization completed")
    except Exception as e:
        print(f"⚠️ Speaker diarization failed: {e}")
        print("⚠️ Continuing without speaker diarization")
        # Add default speaker labels
        for segment in result["segments"]:
            segment["speaker"] = "UNABLE_TO_IDENTIFY"

    # Create output directory with subfolder for this audio file
    base_filename = os.path.splitext(os.path.basename(audio_file))[0]
    output_dir = os.path.join("./output/", base_filename)
    os.makedirs(output_dir, exist_ok=True)

    # Save results in multiple formats (similar to whisperx CLI)
    # JSON format
    import json

    json_path = os.path.join(output_dir, f"{base_filename}.json")
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)

    # TXT format
    txt_path = os.path.join(output_dir, f"{base_filename}.txt")
    with open(txt_path, "w") as f:
        for segment in result["segments"]:
            speaker = segment.get("speaker", "UNKNOWN_SPEAKER")
            f.write(f"[{speaker}] {segment['text']}\n")

    # SRT format
    srt_path = os.path.join(output_dir, f"{base_filename}.srt")
    with open(srt_path, "w") as f:
        for i, segment in enumerate(result["segments"], 1):
            start_time = format_time_srt(segment["start"])
            end_time = format_time_srt(segment["end"])
            speaker = segment.get("speaker", "UNKNOWN_SPEAKER")
            f.write(
                f"{i}\n{start_time} --> {end_time}\n[{speaker}] {segment['text']}\n\n"
            )

    # VTT format
    vtt_path = os.path.join(output_dir, f"{base_filename}.vtt")
    with open(vtt_path, "w") as f:
        f.write("WEBVTT\n\n")
        for segment in result["segments"]:
            start_time = format_time_vtt(segment["start"])
            end_time = format_time_vtt(segment["end"])
            speaker = segment.get("speaker", "UNKNOWN_SPEAKER")
            f.write(f"{start_time} --> {end_time}\n[{speaker}] {segment['text']}\n\n")

    # TSV format
    tsv_path = os.path.join(output_dir, f"{base_filename}.tsv")
    with open(tsv_path, "w") as f:
        f.write("start\tend\tspeaker\ttext\n")
        for segment in result["segments"]:
            speaker = segment.get("speaker", "UNKNOWN_SPEAKER")
            f.write(
                f"{segment['start']:.3f}\t{segment['end']:.3f}\t{speaker}\t{segment['text']}\n"
            )

    print(f"✅ Transcription complete! Files saved to {output_dir}")
    print(f"📄 Files created:")
    print(f"   - {json_path}")
    print(f"   - {txt_path}")
    print(f"   - {srt_path}")
    print(f"   - {vtt_path}")
    print(f"   - {tsv_path}")


def format_time_srt(seconds):
    """Format time for SRT subtitle format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


def format_time_vtt(seconds):
    """Format time for VTT subtitle format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_file>")
        print("Example: python main.py data/70968/61-70968-0000.flac")
    else:
        main(sys.argv[1])
