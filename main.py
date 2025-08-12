import os
import mimetypes
from mp3_stripping import extract_mp3
from transcriber import transcribe


def main():
    while True:
        folder_path = input("Input the relative folder path: ")
        # Convert relative path to absolute path
        absolute_path = os.path.abspath(folder_path)
        process(absolute_path)


def find_files_by_type(folder_path):
    """
    Scan folder recursively and categorize files by type.
    Returns dictionaries of file lists by type.
    """
    video_files = []
    audio_files = []
    document_files = []
    unknown_files = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Get file extension and MIME type
            file_ext = os.path.splitext(filename)[1].lower()
            mime_type, _ = mimetypes.guess_type(filename)

            # Categorize files by type
            if mime_type and mime_type.startswith("video/"):
                video_files.append(file_path)
            elif mime_type and mime_type.startswith("audio/"):
                audio_files.append(file_path)
            elif file_ext in [".pdf", ".png", ".pptx", ".ppt"]:
                document_files.append(file_path)
            else:
                unknown_files.append((file_path, file_ext))

    return video_files, audio_files, document_files, unknown_files


def handle_video_files(video_files, context_file):
    """
    Process video files - convert them to audio format.
    """
    print(f"\n=== Processing {len(video_files)} video files ===")

    audio_files = []

    for video_file in video_files:
        print(f"Converting video to audio: {video_file}")
        audio_files.append(extract_mp3(video_file))


def handle_audio_files(audio_files, context_file):
    """
    Process audio files.
    """
    print(f"\n=== Processing {len(audio_files)} audio files ===")

    transcription_folders = []

    for audio_file in audio_files:
        print(f"Processing audio file: {audio_file}")
        transcription_folder = transcribe(audio_file)
        transcription_folders.append(transcription_folder)

    for folder in transcription_folders:
        if os.path.exists(folder) and os.path.isdir(folder):
            # Get the audio name from the folder name
            audio_name = os.path.basename(folder)

            # Construct the expected txt file path
            expected_txt_file = os.path.join(folder, f"{audio_name}.txt")

            if os.path.exists(expected_txt_file):
                print(f"Found transcription file: {expected_txt_file}")

                # Write transcription to context file
                context_file.write(f"=== {audio_name}.txt ===\n")
                try:
                    with open(expected_txt_file, "r", encoding="utf-8") as txt_file:
                        transcription_content = txt_file.read()
                        context_file.write(transcription_content)
                        context_file.write("\n\n\n")
                except Exception as e:
                    print(f"Error reading transcription file {expected_txt_file}: {e}")
                    context_file.write(f"Error reading file: {e}\n\n\n")

            else:
                print(
                    f"Warning: Expected transcription file not found: {expected_txt_file}"
                )


def handle_document_files(document_files, context_file):
    """
    Process document/presentation files.
    """
    print(f"\n=== Processing {len(document_files)} document files ===")
    for doc_file in document_files:
        print(f"Processing document/presentation file: {doc_file}")
        # TODO: Add document processing logic here


def handle_unknown_files(unknown_files):
    """
    Handle unknown file types - display error and exit.
    """
    if unknown_files:
        print(f"\n=== Error: Found {len(unknown_files)} unsupported files ===")
        for file_path, file_ext in unknown_files:
            print(f"Error: Unknown file type '{file_path}' (extension: {file_ext})")

        print("\nAccepted file types:")
        print("  - Audio files (any audio format)")
        print("  - Video files (any video format)")
        print("  - Documents/Presentations: .pdf, .png, .pptx, .ppt")
        print(
            "\nPlease convert or remove unsupported files from the folder and try again."
        )
        exit(1)


def process(folder_path):
    """
    Main processing function that orchestrates the file processing workflow.
    """
    # Check if folder exists

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        exit(1)

    # Create base filename from folder path
    base_filename = os.path.basename(os.path.normpath(folder_path))
    output_dir = os.path.join("./output/", base_filename)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open context.txt file for writing
    context_file_path = os.path.join(output_dir, "context.txt")
    with open(context_file_path, "w") as context_file:

        # Find and categorize all files
        print(f"Scanning folder: {folder_path}")
        video_files, audio_files, document_files, unknown_files = find_files_by_type(
            folder_path
        )

        # Check for unknown files first and exit if any found
        handle_unknown_files(unknown_files)

        # Process files in order: video -> audio -> documents
        # 1. Convert video files to audio first
        if video_files:
            handle_video_files(video_files, context_file)

        # 2. Process all audio files (including converted ones)
        if audio_files:
            handle_audio_files(audio_files, context_file)

        # 3. Process document files
        if document_files:
            handle_document_files(document_files, context_file)

    print(f"\n=== Processing complete ===")
    print(f"Total files processed:")
    print(f"  - Videos: {len(video_files)}")
    print(f"  - Audio: {len(audio_files)}")
    print(f"  - Documents: {len(document_files)}")
    print(f"Context file saved to: {context_file_path}")


if __name__ == "__main__":
    # Run main processing
    main()
