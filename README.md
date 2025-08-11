# SummerXAIHackathon-AI4SmarterMeetings

## Setup Instructions

### Prerequisites

- Python 3.9+
- CUDA-capable GPU (recommended for faster processing)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd SummerXAIHackathon-AI4SmarterMeetings
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Hugging Face access:**

   a. **Create a READ access token:**

   - Go to [Hugging Face Token Settings](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Select "Read" access type
   - Copy the generated token

   b. **Accept required user agreements:**

   - Accept the user agreement at: [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)
   - Accept the user agreement at: [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)

   c. **Create environment file:**

   - Create a `.env` file in the project root and add your token:

   ```bash
   # In .env file
   HF_TOKEN=your_huggingface_token_here
   ```

### Usage

**Transcribe an audio file:**

```bash
python main.py <audio_file_path>
```

**Example:**

```bash
python main.py data/70968/61-70968-0000.flac
```

The script will generate multiple output formats in the `./output/` directory:

- JSON (detailed transcription with timestamps)
- TXT (simple text with speaker labels)
- SRT (subtitle format)
- VTT (WebVTT subtitle format)
- TSV (tab-separated values with timing data)

---

## Project Ideas

Ideas:

1. Docker for platform independent executible.

2. WhisperX for:

   1. Speech Recognition -> mp3 to text.
   2. labeling people
   3. timestamps

3. AI model for:

   1. Summarization
   2. searching the transcription:
      (what did Pekka say about x? or What was the topic discussed around the 1 hour mark.)

4. UI/UX

   1. Way to label people. ID -> Name.
   2. input pdfs / pngs / mp3s
   3. talk to AI model for questioning.
