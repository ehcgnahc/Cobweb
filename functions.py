import re

def simplify_text(text):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    text = text.replace("\t", "")
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(_)(.?)\1", r"\2", text)
    text = re.sub(r"[\x00-\x1F\u200b]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # print(text)
    return text