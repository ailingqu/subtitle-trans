from googletrans import Translator


def google_translate(transcribe_result, dest_lange: str):
    translator = Translator()
    # language = transcribe_result["language"]
    segments = transcribe_result["segments"]
    for segment in segments:
        text = segment["text"]
        translated = translator.translate(text, dest=dest_lange).text
        segment["translated"] = translated
    return transcribe_result
