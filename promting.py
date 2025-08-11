# gemma3_Modelfile_generator

def generate_config(context_path, output_path):
    # Read speaker context from the input file
    with open(context_path, 'r', encoding='utf-8') as f:
        speaker_context = f.read()

    # Define the Gemma 3 prompt content
    gemma_prompt = f"""FROM gemma3

SYSTEM \"\"\"
You are an assistant with access to the following context:

{speaker_context}
\"\"\"

TEMPLATE \"\"\"
{{{{ if .System }}}}&lt;|im_start|&gt;system
{{{{ .System }}}}&lt;|im_end|&gt;{{{{ end }}}}
{{{{ if .Prompt }}}}&lt;|im_start|&gt;user
{{{{ .Prompt }}}}&lt;|im_end|&gt;{{{{ end }}}}
&lt;|im_start|&gt;assistant
\"\"\"
"""

    # Write the prompt to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(gemma_prompt)

    print(f"Gemma 3 Modelfile file has been generated and saved as '{output_path}'.")


if __name__ == "__main__": 
    # Example usage 
    generate_config("/home/mainguye/ai-hack-SX/.local/transcript.txt", "Modelfile")
