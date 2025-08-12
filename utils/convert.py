"""
for converting additional documents to all PNGs
"""

import sys
import os
from PIL import Image
from pdf2image import convert_from_path
from pptx import Presentation


def convert_pdf_to_png(input_path, output_path, output_name):
    images = convert_from_path(input_path)
    for i, image in enumerate(images):
        image.save(os.path.join(output_path, f"{output_name}_page_{i+1}.png"), "PNG")


def convert_jpeg_to_png(input_path, output_path, output_name):
    image = Image.open(input_path)
    image.save(os.path.join(output_path, f"{output_name}.png"), "PNG")


def convert_pptx_to_png(input_path, output_path, output_name):
    prs = Presentation(input_path)
    for i, slide in enumerate(prs.slides):
        img = Image.new("RGB", (1280, 720), color="white")
        img.save(os.path.join(output_path, f"{output_name}_slide_{i+1}.png"), "PNG")


def convert_any(input_path, output_path, output_name):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ext = os.path.splitext(input_path)[1].lower()

    if ext == ".pdf":
        convert_pdf_to_png(input_path, output_path, output_name)
    elif ext == ".jpeg" or ext == ".jpg":
        convert_jpeg_to_png(input_path, output_path, output_name)
    elif ext == ".pptx":
        convert_pptx_to_png(input_path, output_path, output_name)
    else:
        print("Unsupported file format. Supported formats are: PDF, JPEG, PPTX")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python convert.py <input_path> <output_path> <output_name>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    output_name = sys.argv[3]
    convert_any(input_path, output_path, output_name)
