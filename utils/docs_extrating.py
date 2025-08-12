import sys
from PIL import Image
import base64
import ollama
from ollama import chat
from ollama import ChatResponse


def extract_document_content(path_to_images, format_, output_path):
    """
    Extract content from document images using OCR and save to a context file.

    Args:
        path_to_images (str): Path to the image file
        format_ (str): Format of the original document (pdf, png, pptx, etc.)
        output_path (str or file object): Path where the extracted content will be saved, or an open file object

    Returns:
        str: Extracted content from the document
    """
    img = Image.open(path_to_images)
    image_base64_list = []

    # reading image
    with open(path_to_images, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        image_base64_list.append(encoded_string)

    response: ChatResponse = chat(
        model="ocr-er",
        messages=[
            {
                "role": "user",
                "content": "Extract all the information from the image word by word",
                "images": image_base64_list,
            },
        ],
    )
    print(response["message"]["content"])
    result = response["message"]["content"]

    if format_ == "pdf" or format_ == "PDF":
        context = f"[PDF DOCUMENT]: {result}"

    elif format_ == "png" or format_ == "PNG":
        context = f"[PNG DOCUMENT]: {result}"

    elif format_ == "pptx" or format_ == "PPTX":
        context = f"[POWERPOINT DOCUMENT]: {result}"

    # Write to the output file or file object
    if hasattr(output_path, "write"):
        # output_path is a file object
        output_path.write(context + "\n\n")
        print(f"Additional document content has been written to the context file.")
    else:
        # output_path is a file path string
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(context)
        print(
            f"Additional document as context file has been generated and saved as '{output_path}'."
        )

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python docs_extracting.py <path_to_images> <original_format>")
        sys.exit(1)

    path_to_images = sys.argv[1]
    format_ = sys.argv[2]

    # Extract document content using the function
    extract_document_content(path_to_images, format_, "./context/additional_docs.txt")
