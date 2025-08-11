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

**Important Notes:**

- **Each user must accept the agreements individually** - sharing tokens violates Hugging Face terms of service
- **Personal tokens only** - Do not share your token or use someone else's token
- **For CI/CD**: Use GitHub repository secrets, but ensure the account that generated the token has accepted the required agreements

### Usage

**1. Extract sample audio data:**

```bash
cd data
unzip audio_1.zip
mv 70*/ audio_1/
```

This will extract the audio files to `data/audio_1/` directory.

**2. Transcribe an audio file:**

```bash
python main.py <audio_file_path>
```

**Examples:**

```bash
# Using the extracted sample data
python main.py data/audio_1/61-70968-0001.flac
```

The script will generate multiple output formats in the `./output/` directory:

- JSON (detailed transcription with timestamps)
- TXT (simple text with speaker labels)
- SRT (subtitle format)
- VTT (WebVTT subtitle format)
- TSV (tab-separated values with timing data)

### GitHub Actions / CI/CD Usage

For automated workflows, you can use GitHub repository secrets:

1. **Set up repository secret:**

   - Go to your repository Settings → Secrets and variables → Actions
   - Add a new secret named `HF_TOKEN` with your token value

2. **Example workflow:**
   ```yaml
   # .github/workflows/transcribe.yml
   name: Transcribe Audio
   on: [push]
   jobs:
     transcribe:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: "3.9"
         - name: Install dependencies
           run: pip install -r requirements.txt
         - name: Transcribe
           env:
             HF_TOKEN: ${{ secrets.HF_TOKEN }}
           run: python main.py data/audio.flac
   ```

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
