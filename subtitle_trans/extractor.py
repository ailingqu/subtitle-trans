from pathlib import Path

import whisperx
from whisperx.asr import FasterWhisperPipeline

print_progress = True


# Extractor for subtitles from audio
class Extractor:
    device: str
    batch_size: int
    compute_type: str
    download_root: str
    whisperx_model: FasterWhisperPipeline

    def __init__(self,
                 # cuda or cpu
                 device="cpu",
                 device_index=0,
                 # float16 or int8
                 compute_type="int8",
                 # large-v2 or large-v3
                 model="large-v2"):
        self.device = device
        self.compute_type = compute_type
        self.download_root = f"{Path.home()}/models"
        self.whisperx_model = whisperx.load_model(model, device, device_index=device_index, compute_type=compute_type,
                                                  download_root=self.download_root, threads=16)

    def transcribe(self, audio_file: str, batch_size: int, use_auth_token: str):
        audio = whisperx.load_audio(audio_file)
        result = self.whisperx_model.transcribe(audio, batch_size=batch_size, print_progress=print_progress,
                                                combined_progress=print_progress)
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device,
                                                      model_dir=self.download_root)
        result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False,
                                print_progress=print_progress, combined_progress=print_progress)
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=use_auth_token,
                                                     device=self.device)
        diarize_segments = diarize_model(audio)
        return whisperx.assign_word_speakers(diarize_segments, result)
