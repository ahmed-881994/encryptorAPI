from typing import Dict
from . import lookups
# handles Arabic letters variants
def handleArabicVariants(chars: list[str])-> list[str]:
    for char in chars:
        if char in ['أ','ء','ئ','ى','آ','إ']:
            chars[chars.index(char)] = 'ا'
        elif char == 'ة':
            chars[chars.index(char)] = 'ت'
        elif char == 'ؤ':
            chars[chars.index(char)] = 'و'
    return chars

def encryptCaesar(plainText: str, lang: str, shift: int) -> Dict:
    cypherText = ""
    plainText=plainText.upper()
    chars = list(plainText)
    if lang == 'AR':
        chars = handleArabicVariants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ": # handles empty space
                cypherText += " "
            elif (
                char in lookups.alphabets["AR"]["numbers"]
                or char in lookups.alphabets["EN"]["numbers"]
            ): # handles numbers
                cypherText += char
            elif char in lookups.alphabets["SpecialCharacters"]: # removes special characters
                pass
            else: # encrypts
                index = lookups.alphabets[lang]["letters"].index(char)
                shiftedIndex = lookups.alphabets[lang]["letters"].index(char) + shift
                if lang == "EN":
                    if shiftedIndex > 25:
                        shiftedIndex -= 26
                elif lang == "AR":
                    if shiftedIndex > 27:
                        shiftedIndex -= 28
                print(char,index,shiftedIndex)
                cypherText += lookups.alphabets[lang]["letters"][shiftedIndex]
        return {"status": 200, "cypherText": cypherText}
    else:
        return {"status": 400, "detail": "Plain text and language choice don't match"}


def encryptMorse(plainText: str, lang: str)-> Dict:
    cypherText = ""
    plainText=plainText.upper()
    chars = list(plainText)
    if lang == 'AR':
        chars = handleArabicVariants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ": # handles empty space
                cypherText += '/'
            elif char == '.': # handles end of sentence
                cypherText += '//'
            elif char in lookups.alphabets["SpecialCharacters"]: # removes special characters
                pass
            elif (
                char in lookups.alphabets["AR"]["numbers"]
                or char in lookups.alphabets["EN"]["numbers"]
            ): # handles numbers
                if char in lookups.alphabets["AR"]["numbers"]:
                    cypherText+= lookups.alphabets['Morse']['Numbers'][lookups.alphabets['AR']["numbers"].index(char)]
                elif char in lookups.alphabets["EN"]["numbers"]:
                    cypherText+= lookups.alphabets['Morse']['Numbers'][lookups.alphabets['EN']["numbers"].index(char)]
            else:
                cypherText+= lookups.alphabets['Morse'][lang][lookups.alphabets[lang]["letters"].index(char)]
        return {"status": 200, "cypherText": cypherText}
    else:
        return {"status": 400, "detail": "Plain text and language choice don't match"}


def encryptNumeric(plainText: str, lang: str)-> Dict:
    cypherText = ""
    plainText=plainText.upper()
    chars = list(plainText)
    if lang == 'AR':
        chars = handleArabicVariants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ": # handles empty space
                cypherText += '/'
            elif char == '.': # handles end of sentence
                cypherText += '//'
            elif char in lookups.alphabets["SpecialCharacters"]: # removes special characters
                pass
            elif (
                char in lookups.alphabets["AR"]["numbers"]
                or char in lookups.alphabets["EN"]["numbers"]):
                pass
            else:
                number = lookups.alphabets[lang]["letters"].index(char)+1
                cypherText+= str(number)
        return {"status": 200, "cypherText": cypherText}
    else:
        return {"status": 400, "detail": "Plain text and language choice don't match"}


def encryptReverseNumeric(plainText: str, lang: str)-> Dict:
    cypherText = ""
    plainText=plainText.upper()
    chars = list(plainText)
    if lang == 'AR':
        chars = handleArabicVariants(chars)
    if chars[0] in lookups.alphabets[lang]["letters"] or chars[0] in lookups.alphabets["AR"]["numbers"] or chars[0] in lookups.alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ": # handles empty space
                cypherText += '/'
            elif char == '.': # handles end of sentence
                cypherText += '//'
            elif char in lookups.alphabets["SpecialCharacters"]: # removes special characters
                pass
            elif (
                char in lookups.alphabets["AR"]["numbers"]
                or char in lookups.alphabets["EN"]["numbers"]):
                pass
            else:
                number = lookups.alphabets[lang]["reverseLetters"].index(char)+1
                cypherText+= str(number)
        return {"status": 200, "cypherText": cypherText}
    else:
        return {"status": 400, "detail": "Plain text and language choice don't match"}
