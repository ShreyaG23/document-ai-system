from transformers import pipeline
from typing import List

_SUMMARIZER = None

def _get_summarizer():
    global _SUMMARIZER
    if _SUMMARIZER is None:
        # load a summarizer model
        _SUMMARIZER = pipeline("summarization",model="sshleifer/distilbart-cnn-12-6")

    return _SUMMARIZER

def _chunk_text_by_words(text: str, max_words: int = 800) ->List[str]:
    """
    Docstring for _chunk_text_by_words
    
    :param text: Description
    :type text: str
    :param max_words: Description
    :type max_words: int
    :return: Description
    :rtype: List[str]

    Simple chunker: split text by words into chunks of ~max_words length.
    Keeps sentence boundaries roughly (naive).
    """
    words = text.split()
    if len(words) <= max_words:
        return [text]
    chunks =[]
    i = 0
    while i < len(words):
        chunk = words[i:i+max_words]
        chunks.append("".join(chunk))
        i += i+max_words
    return chunks

def summarize_text(text:str, max_length: int=250, min_length: int = 100) -> str:
    """
    summazise text, if it is too long it will chunk summarize and combined summarize version again to get precise one

    """
    if not text or not text.strip():
        return ""
    summarizer = _get_summarizer()

    #chunk the text to avoid input length issues
    chunks = _chunk_text_by_words(text, max_words=300)

    #summarize each chunk
    chunk_summarise = []
    for c in chunks:
        out = summarizer(c, max_length = max_length, min_length=min_length, do_sample = False)
        if isinstance(out, list) and len(out)>0:
            chunk_summarise.append(out[0].get("summary_text", ""))
        else:
            #fallback: return prefix if summarizer fails
            print("summarizer fails")
            chunk_summarise.append(c[:max_length*4])
    #if only 1 chunk
    if len(chunk_summarise) == 1:
        return chunk_summarise[0].strip()
    
    #else combine and summarize again
    combined = " ".join(chunk_summarise)

    if len(combined) > 300:
        combined = " ".join(combined.split()[:300])
    final = summarizer(combined, max_length=max_length, min_length=min_length, do_sample = False)
    if isinstance(final, list) and len(final)>0:
        return final[0].get("summary_text", "")
    return combined.strip()
