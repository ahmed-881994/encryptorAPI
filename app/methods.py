from typing import Dict
from . import lookups
# handles Arabic letters variants


def handle_arabic_variants(chars: list[str]) -> list[str]:
    """Handles variants of the Arabic letters and returns a default value for similar variants

    Args:
        chars (list[str]): The plain text to be cleaned

    Returns:
        list[str]: Cleaned plain text
    """
    for char in chars:
        if char in ['أ', 'ء', 'ئ', 'ى', 'آ', 'إ']:
            chars[chars.index(char)] = 'ا'
        elif char == 'ة':
            chars[chars.index(char)] = 'ت'
        elif char == 'ؤ':
            chars[chars.index(char)] = 'و'
    return chars


def encrypt_caesar(plain_text: str, lang: str, shift: int) -> Dict:
    """Encrypts plain text using the Caesar encryption

    Args:
        plain_text (str): Plain text to be encrypted
        lang (str): Language of plain text
        shift (int): The shift value

    Returns:
        Dict: Encrypted text
    """
    cypher_text = ""
    plain_text = plain_text.upper()
    chars = list(plain_text)
    if lang == 'AR':
        chars = handle_arabic_variants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += " "
            elif (
                char in lookups.alphabets["AR"]["numbers"]
                or char in lookups.alphabets["EN"]["numbers"]
            ):  # handles numbers
                cypher_text += char
            # removes special characters
            elif char in lookups.alphabets["SpecialCharacters"]:
                pass
            else:  # encrypts
                shifted_index = lookups.alphabets[lang]["letters"].index(
                    char) + shift
                if lang == "EN":
                    if shifted_index > 25:
                        shifted_index -= 26
                elif lang == "AR":
                    if shifted_index > 27:
                        shifted_index -= 28
                cypher_text += lookups.alphabets[lang]["letters"][shifted_index]
        return {"status": 200, "cypher_text": cypher_text.strip()}
    else:
        return {"status": 400, "msg": "Plain text and language choice don't match"}


def encrypt_morse(plain_text: str, lang: str) -> Dict:
    """Encrypts plain text using the Morse encryption

    Args:
        plain_text (str): Plain text to be encrypted
        lang (str): Language of plain text

    Returns:
        Dict: Encrypted text
    """
    cypher_text = ""
    plain_text = plain_text.upper()
    chars = list(plain_text)
    if lang == 'AR':
        chars = handle_arabic_variants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += '/'
            elif char == '.':  # handles end of sentence
                cypher_text += '//'
            # removes special characters
            elif char in lookups.alphabets["SpecialCharacters"]:
                pass
            elif (
                char in lookups.alphabets["AR"]["numbers"]
                or char in lookups.alphabets["EN"]["numbers"]
            ):  # handles numbers
                if char in lookups.alphabets["AR"]["numbers"]:
                    cypher_text += ' ' + \
                        lookups.alphabets['Morse']['Numbers'][lookups.alphabets['AR']["numbers"].index(
                            char)]
                elif char in lookups.alphabets["EN"]["numbers"]:
                    cypher_text += ' ' + \
                        lookups.alphabets['Morse']['Numbers'][lookups.alphabets['EN']["numbers"].index(
                            char)]
            else:
                cypher_text += ' ' + \
                    lookups.alphabets['Morse'][lang][lookups.alphabets[lang]["letters"].index(
                        char)]
        return {"status": 200, "cypher_text": cypher_text.strip()}
    else:
        return {"status": 400, "msg": "Plain text and language choice don't match"}


def encrypt_numeric(plain_text: str, lang: str) -> Dict:
    """Encrypts plain text using the Numeric encryption

    Args:
        plain_text (str): Plain text to be encrypted
        lang (str): Language of plain text

    Returns:
        Dict: Encrypted text
    """
    cypher_text = ""
    plain_text = plain_text.upper()
    chars = list(plain_text)
    if lang == 'AR':
        chars = handle_arabic_variants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += '/'
            elif char == '.':  # handles end of sentence
                cypher_text += '//'
            # removes special characters
            elif char in lookups.alphabets["SpecialCharacters"]:
                pass
            elif (
                    char in lookups.alphabets["AR"]["numbers"]
                    or char in lookups.alphabets["EN"]["numbers"]):
                pass
            else:
                number = lookups.alphabets[lang]["letters"].index(char)+1
                cypher_text += ' ' + str(number)
        return {"status": 200, "cypher_text": cypher_text.strip()}
    else:
        return {"status": 400, "msg": "Plain text and language choice don't match"}


def encrypt_reverse_numeric(plain_text: str, lang: str) -> Dict:
    """Encrypts plain text using the reverse Numeric encryption

    Args:
        plain_text (str): Plain text to be encrypted
        lang (str): Language of plain text

    Returns:
        Dict: Encrypted text
    """
    cypher_text = ""
    plain_text = plain_text.upper()
    chars = list(plain_text)
    if lang == 'AR':
        chars = handle_arabic_variants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += '/'
            elif char == '.':  # handles end of sentence
                cypher_text += '//'
            # removes special characters
            elif char in lookups.alphabets["SpecialCharacters"]:
                pass
            elif (
                    char in lookups.alphabets["AR"]["numbers"]
                    or char in lookups.alphabets["EN"]["numbers"]):
                pass
            else:
                number = lookups.alphabets[lang]["reverseLetters"].index(
                    char)+1
                cypher_text += ' ' + str(number)
        return {"status": 200, "cypher_text": cypher_text.strip()}
    else:
        return {"status": 400, "msg": "Plain text and language choice don't match"}


def encode_NATO(plain_text: str) -> Dict:
    """Encodes input text in the NATO phonetic alphabet

    Args:
        plain_text (str): Plain text to be encoded

    Returns:
        Dict: Encrypted text
    """
    cypher_text = ""
    plain_text = plain_text.upper()
    chars = list(plain_text)
    if chars[0] in lookups.alphabets['EN']["letters"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char in lookups.alphabets["EN"]["numbers"]:
                code = lookups.alphabets['NATONumbers'][lookups.alphabets['EN']["numbers"].index(
                    char)]
                cypher_text += ' ' + str(code)
            elif char == ' ':
                cypher_text += ' (space)'
            elif char in lookups.alphabets["SpecialCharacters"]:
                pass
            else:
                code = lookups.alphabets['NATOLetters'][lookups.alphabets['EN']["letters"].index(
                    char)]
                cypher_text += ' ' + str(code)
        return {"status": 200, "cypher_text": cypher_text.strip()}
    else:
        return {"status": 400, "msg": "This method only supports English characters"}
