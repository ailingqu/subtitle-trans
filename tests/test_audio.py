import json

from subtitle_trans.extractor import Extractor


def test_transcribe():
    extractor = Extractor()
    audio_file = "test_audio_cn.mp3"
    result = extractor.transcribe(audio_file, 16)
    print(json.dumps(result))
    result = extractor.align(audio_file, result)
    print(json.dumps(result))
    result = extractor.classify(audio_file, "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", result)
    print(json.dumps(result))


test_transcribe()
