from konlpy.tag import Twitter; t = Twitter()

def tokenizer(text):
    tk = t.morphs(text)
    return tk
