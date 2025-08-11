This repository contains example scripts and data to experiment with a Smart Meeting Agent pipeline for speech recognition and downstream text processing.

**📁 About the Data**

The data/ folder includes two .zip files. Each zip archive contains:

.flac files – short audio segments (a few seconds each)
.txt files – transcripts corresponding to each audio file

**📚 Source**

The data is sourced from LibriSpeech, a public-domain corpus of read speech derived from LibriVox audiobooks.
LibriSpeech is designed to support research and development in automatic speech recognition (ASR).

For more information related to the dataset and its subset, please visit: 
https://www.openslr.org/12

Please note that the example code can be run smoothly and it will generate text for the audio. 



**🚀 Prerequisites**

To run this starter code, you will need: 

- Python 3.11 or higher. 

```bash
module load  biopythontools/11.3.0_3.10.6_1.76
```

**🔧 Installation**

1. Clone this repository
2. Create an environment and install dependencies. Dependencies can be listed either in requirements.txt (for local implementation) or in env.yml (for Puhti implementation).

For local usage, you can either use python virtual environment or conda environment. Example below is for python virtual environment.

```bash 
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```

For usage on Puhti, it is recommended to use Tykky container wrapper.

```bash
module purge
module load tykky
mkdir <install_dir>
conda-containerize new --prefix <install_dir> env.yml
export PATH="<install_dir>/bin:$PATH"
```


**🛠️ What the Python Scripts Do**

➡️ transcriber.py: Defines a Transcriber class that uses the Faster-Whisper ASR model to convert audio files (.flac, .wav, etc.) into plain English text. You can specify model size (e.g., "base", "small") and language.


➡️ main.py: Runs the full pipeline: takes an audio file path as input, uses the Transcriber to generate a transcript, and prints the transcript to the console. Example usage:




```bash
python3 main.py audio.flac
```


**🧑‍🏫 What you have to-do?**

Surprise us by being creative in creating ai-agent that can listen to audio chats and convert it to text and also summarize the meeting. For simplicity, a starter code that convert audio into text has been provided for you. The dataset contains both audio and text so you can do more adventures. 



**📝 License**

This project is licensed under the MIT License - see the LICENSE file for details.

**💼 Variables to tune**

Feel free to change. 
