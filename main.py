import argparse
import os
import mimetypes


def cli_ui_loop():
    while True:
        input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI for Smarter Meetings")
    parser.add_argument("data_folder", help="Path to the data folder")

    args = parser.parse_args()
    folder_path = args.data_folder

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        exit(1)

    # Iterate through files in the folder recursively
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Get file extension and MIME type
            file_ext = os.path.splitext(filename)[1].lower()
            mime_type, _ = mimetypes.guess_type(filename)

            # Check file types
            if mime_type and mime_type.startswith("audio/"):
                print(f"Audio file: {file_path}")
                # Process audio file
            elif mime_type and mime_type.startswith("video/"):
                print(f"Video file: {file_path}")
                # Process video file
            elif file_ext in [".pdf", ".png", ".pptx", ".ppt"]:
                print(f"Document/Presentation file: {file_path}")
                # Process document/presentation file
            else:
                print(f"Error: Unknown file type '{file_path}' (extension: {file_ext})")
                print("Accepted file types:")
                print("  - Audio files (any audio format)")
                print("  - Video files (any video format)")
                print("  - Documents/Presentations: .pdf, .png, .pptx, .ppt")
                print(
                    "\nPlease convert or remove unsupported files from the folder and try again."
                )
                exit(1)

    cli_ui_loop()
