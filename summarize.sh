# setup ollama model
ollama -v

# pulling model
ollama pull $MODEL_ID

# setting up Modelfile config for model
python prompting.py -c $TRANSCRIPT_PATH

# create ollama model
ollama create listener -f Modelfile

# run the listener
ollama run listener