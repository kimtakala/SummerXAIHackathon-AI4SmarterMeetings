from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(model_size, compute_type="int8")

    def transcribe(self, audio_path, language="en"):
        segments, _ = self.model.transcribe(audio_path, language=language)
        full_text = " ".join(segment.text for segment in segments)
        return full_text
