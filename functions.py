import re
import unicodedata
import emoji

def normalize_text(text):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    text = text.replace("\t", "")
    text = text.upper()
    text = re.sub(r"[_]", "", text)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(_)(.?)\1", r"\2", text)
    text = re.sub(r"[\x00-\x1F\u200b\u200d]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = emoji.replace_emoji(text, replace="")
    text = ''.join(unicodedata.normalize('NFKD', char) for char in text)
    return text