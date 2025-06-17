import unicodedata
import re

CHARACTER_MAP = {
    'ø': 'oe',
    'Ø': 'Oe',
    'å': 'a',
    'Å': 'a',
    'ä': 'ae',
    'Ä': 'Ae',
    'ö': 'oe',
    'Ö': 'Oe',
    'é': 'e',
    'É': 'E',
    'á': 'a',
    'Á': 'A',
    'í': 'i',
    'Í': 'I',
    'ó': 'o',
    'Ó': 'O',
    'ú': 'u',
    'Ú': 'U',
    'ñ': 'n',
    'Ñ': 'N',
    'ç': 'c',
    'Ç': 'C',
    'ß': 'ss',
    'č': 'c',
    'Č': 'C',
    'š': 's',
    'Š': 'S',
    'ž': 'z',
    'Ž': 'Z',
}

def flatten(text: str) -> str:
    """
    Converts Unicode strings to ASCII with smart transliteration for key characters.
    Ex: 'Mikkel Bødker' → 'Mikkel Boedker'
    """

    def name_case(name):
        return ' '.join(word.capitalize() for word in name.split())
    # First apply manual character map
    for char, replacement in CHARACTER_MAP.items():
        text = text.replace(char, replacement)

    # Then remove any remaining diacritics via Unicode normalization
    normalized = unicodedata.normalize('NFKD', text)
    ascii_bytes = normalized.encode('ascii', 'ignore')
    flat_text = ascii_bytes.decode('ascii')

    return name_case(re.sub(r'\s+', ' ', flat_text).strip())