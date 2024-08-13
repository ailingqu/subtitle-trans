from subtitle_trans.extractor import Extractor


def test_transcribe():
    extractor = Extractor()
    result = extractor.transcribe("test_audio.mp3", 16, "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")
    print(result)
