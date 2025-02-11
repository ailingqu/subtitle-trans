from pathlib import Path

import torch
import whisperx
from whisperx.asr import FasterWhisperPipeline
from whisperx.utils import format_timestamp

print_progress = True


# Extractor for subtitles from audio
class Extractor:
    device: str
    device_index: int
    compute_type: str
    download_root: str

    def __init__(self,
                 # cuda or cpu
                 device="cuda" if torch.cuda.is_available() else "cpu",
                 device_index=0,
                 # float16 or int8 or float32
                 compute_type="float32" if torch.cuda.is_available() else "int8"):
        self.device = device
        self.device_index = device_index
        self.compute_type = compute_type
        self.download_root = f"{Path.home()}/models"

    def transcribe(self, audio_file: str, batch_size: int,
                   # large-v2 or large-v3
                   model="large-v3"):
        whisperx_model = whisperx.load_model(model, self.device, device_index=self.device_index,
                                             compute_type=self.compute_type,
                                             download_root=self.download_root, threads=batch_size)
        audio = whisperx.load_audio(audio_file)
        return whisperx_model.transcribe(audio, batch_size=batch_size, print_progress=print_progress)

    def align(self, audio_file: str, transcribe_result):
        model_a, metadata = whisperx.load_align_model(language_code=transcribe_result["language"], device=self.device,
                                                      model_dir=self.download_root)
        audio = whisperx.load_audio(audio_file)
        return whisperx.align(transcribe_result["segments"], model_a, metadata, audio, self.device,
                              return_char_alignments=False,
                              print_progress=print_progress)

    def classify(self, audio_file: str, use_auth_token: str, transcribe_result):
        model = whisperx.DiarizationPipeline(use_auth_token=use_auth_token,
                                             device=self.device)
        audio = whisperx.load_audio(audio_file)
        segments = model(audio)
        return whisperx.assign_word_speakers(segments, transcribe_result)

    def write_srt_file(self, transcribe_result, out_file: str):
        with open(out_file, 'w', encoding='utf-8') as f:
            segments = transcribe_result["segments"]
            for index, segment in enumerate(segments):
                line = (f"{index}\n{format_timestamp(segment['start'], always_include_hours=True)} "
                        f"--> {format_timestamp(segment['end'], always_include_hours=True)}\n"
                        f"{str(segment['text']).strip()}\n")
                if "translated" in segment:
                    line += f"{str(segment['translated'])}\n"
                line += "\n"
                f.write(line)
