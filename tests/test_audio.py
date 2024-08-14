import json
import os

from subtitle_trans import translator
from subtitle_trans.extractor import Extractor


def test_transcribe():
    extractor = Extractor()
    audio_file = "test_audio_uk.mp3"
    os.makedirs("C:\\Users\\nclai\\git\\subtitle-trans\\srts", exist_ok=True)
    result = extractor.transcribe(audio_file, 16)
    print(json.dumps(result, ensure_ascii=False))
    result = translator.google_translate(result, "zh-cn")
    print(json.dumps(result, ensure_ascii=False))
    extractor.write_srt_file(result, "C:\\Users\\nclai\\git\\subtitle-trans\\srts\\1.srt")
    result = extractor.align(audio_file, result)
    print(json.dumps(result, ensure_ascii=False))
    result = translator.google_translate(result, "zh-cn")
    print(json.dumps(result, ensure_ascii=False))
    extractor.write_srt_file(result, "C:\\Users\\nclai\\git\\subtitle-trans\\srts\\2.srt")
    result = extractor.classify(audio_file, "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", result)
    print(json.dumps(result, ensure_ascii=False))
    result = translator.google_translate(result, "zh-cn")
    print(json.dumps(result, ensure_ascii=False))
    extractor.write_srt_file(result, "C:\\Users\\nclai\\git\\subtitle-trans\\srts\\3.srt")


test_transcribe()
