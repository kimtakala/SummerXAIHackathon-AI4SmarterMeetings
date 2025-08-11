from transcriber import Transcriber
import sys


def main(audio_file):
    print("[1] Transcribing...")
    transcriber = Transcriber()
    transcript = transcriber.transcribe(audio_file)

    print("\n📄 transcript:\n")
    print(transcript)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_file>")
    else:
        main(sys.argv[1])
