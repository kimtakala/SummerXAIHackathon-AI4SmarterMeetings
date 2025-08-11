# setup ollama model
ollama -v

# pulling model
ollama pull $MODEL_ID
# requirement for ocr
ollama pull llama3.2-vision:11b
ollama pull granite3.2-vision
ollama pull moondream
ollama pull minicpm-v

# setting up Modelfile config for model
python utils/prompting.py -c $TRANSCRIPT_PATH

# create ollama model
ollama create listener -f Modelfile

# run the listener
ollama run listener