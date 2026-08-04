import os
from deep_translator import GoogleTranslator

def translate_word(urdu_word):
    try:
        return GoogleTranslator(source="ur", target="en").translate(urdu_word)
    except Exception as e:
        print(f"Error translating '{urdu_word}': {e}")
        return None

def translate_line(urdu_line):
    try:
        return GoogleTranslator(source="ur", target="en").translate(urdu_line)
    except Exception as e:
        print(f"Error translating line: {e}")
        return None

def translate_word_in_context(urdu_word, context_line):
    try:
        # Translate the full line, use it as context
        line_translation = translate_line(context_line)
        word_translation = translate_word(urdu_word)
        return word_translation
    except Exception as e:
        return translate_word(urdu_word)

_U2R = {
    'ا':'a','آ':'aa','ب':'b','پ':'p','ت':'t','ٹ':'T','ث':'s',
    'ج':'j','چ':'ch','ح':'h','خ':'kh','د':'d','ڈ':'D','ذ':'z',
    'ر':'r','ڑ':'R','ز':'z','ژ':'zh','س':'s','ش':'sh','ص':'s',
    'ض':'z','ط':'t','ظ':'z','ع':"'",'غ':'gh','ف':'f','ق':'q',
    'ک':'k','گ':'g','ل':'l','م':'m','ن':'n','ں':'n','و':'w/o',
    'ہ':'h','ھ':'h','ء':"'",'ی':'y','ے':'e','ئ':'y','ؤ':'o',
    'ْ':'','ً':'an','ٌ':'un','ٍ':'in','َ':'a','ُ':'u','ِ':'i',
    'ّ':'','ٰ':'a','۔':'.','،':',','؟':'?'
}

def transliterate_free(urdu_text):
    result = []
    for line in urdu_text.split('\n'):
        roman_line = []
        for word in line.split():
            roman_word = ''.join(_U2R.get(char, char) for char in word)
            roman_line.append(roman_word)
        result.append(' '.join(roman_line))
    return '\n'.join(result)

def transliterate(urdu_text):
    return transliterate_free(urdu_text)