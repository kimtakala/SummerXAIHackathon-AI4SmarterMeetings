import sys
from ollama import chat
from ollama import ChatResponse
from PIL import Image
import ollama
import base64


if __name__=="__main__": 
    if len(sys.argv) != 3:
        print("Usage: python docs_extracting.py <path_to_images> <original_format>")
        sys.exit(1)

    path_to_images = sys.argv[1]
    format_ = sys.argv[2]
    img = Image.open(path_to_images)
    image_base64_list = []

    # reading image
    with open(path_to_images, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        image_base64_list.append(encoded_string)

    ollama.create(model='ocr-er', from_='openbmb/minicpm-o2.6:latest', system="You are a helpful assistant.")

    response: ChatResponse = chat(model='ocr-er', messages=[
    {
        'role': 'user',
        'content': 'Extract all the information from the image word by word',
        'images': image_base64_list
    },
    ])
    print(response['message']['content'])
    result = response['message']['content']

    if format_ == 'pdf' or format_ == 'PDF': 
        context= f"[PDF DOCUMENT]: {result}"

    if format_ == 'png' or format_ == 'PNG': 
        context= f"[PNG DOCUMENT]: {result}"

    if format_ == 'pptx' or format_ == 'PPTX': 
        context= f"[POWERPOINT DOCUMENT]: {result}"

    # Write the prompt to the output file
    output_path = './context/additional_docs.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(context)

    print(f"Additional document as context file has been generated and saved as '{output_path}'.")
    
