from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from mangum import Mangum
from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field

### Schemas###


class lang_enum(str, Enum):

    AR = 'AR'

    EN = 'EN'


class EncryptRq(BaseModel):

    plainText: str = Field(min_length=1)
    language: lang_enum


class EncryptNATORq(BaseModel):

    plainText: str = Field(min_length=1)


class EncryptCaesarRq(EncryptRq):

    shift: int


class EncryptRs(BaseModel):

    cypherText: str


class Detail(BaseModel):
    msg: str


class ErrorRs(BaseModel):
    detail: List[Detail]

######
### API###


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    detail = []
    detail.append(
        {'msg': f'Rate limit exceeded: {exc.detail} Try again in a while...'})
    res = {'detail': detail}
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=res
    )


def get_application() -> FastAPI:
    application = FastAPI(responses={429: {'model': ErrorRs}, 400: {'model': ErrorRs}}, exception_handlers={429: rate_limit_exceeded_handler},
                          title="Encryptor", description="Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.", version="0.1.0")
    return application


app = get_application()
LIMIT = '5/minute'
handler = Mangum(app)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


@app.get("/", include_in_schema=False)
async def health_check():
    """Used to check the status of the app

    Returns:
        JSON: Current status
    """
    return {"Status": "running"}


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse('app/assets/favicon.ico')


@app.post("/caesar", response_model=EncryptRs)
@limiter.limit(LIMIT)
async def caesar(body: EncryptCaesarRq, request: Request):
    """Takes input & validates against schema then encrypts using Caesar encryption & returns result

    Args:
        body (EncryptCaesarRq): Input JSON request

    Raises:
        HTTPException: Error in execution
    Returns:
        JSON: Encrypted text
    """
    result = encrypt_caesar(body.plainText, body.language, body.shift)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/morse", response_model=EncryptRs)
@limiter.limit(LIMIT)
async def morse(body: EncryptRq, request: Request):
    """Takes input & validates against schema then encrypts using Morse encryption & returns result

    Args:
        body (EncryptRq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = encrypt_morse(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/numeric", response_model=EncryptRs)
@limiter.limit(LIMIT)
async def numeric(body: EncryptRq, request: Request):
    """Takes input & validates against schema then encrypts using Numeric encryption & returns result

    Args:
        body (EncryptRq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = encrypt_numeric(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/reversenumeric", response_model=EncryptRs)
@limiter.limit(LIMIT)
async def reverse_numeric(body: EncryptRq, request: Request):
    """Takes input & validates against schema then encrypts using Inverse Numeric encryption & returns result

    Args:
        body (EncryptRq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = encrypt_reverse_numeric(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/natoalphabet", response_model=EncryptRs)
@limiter.limit(LIMIT)
async def nato_alphabet(body: EncryptNATORq, request: Request):
    """Takes input & validates against schema then encodes using NATO alphabet encoding & returns result

    Args:
        body (schemas.EncryptNATORq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = encode_NATO(body.plainText)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}
######
### Methods###
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
    if chars[0] in alphabets[lang]["letters"] or chars[0] in alphabets["AR"]["numbers"] or chars[0] in alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += " "
            elif (
                char in alphabets["AR"]["numbers"]
                or char in alphabets["EN"]["numbers"]
            ):  # handles numbers
                cypher_text += char
            # removes special characters
            elif char in alphabets["SpecialCharacters"]:
                pass
            else:  # encrypts
                shifted_index = alphabets[lang]["letters"].index(
                    char) + shift
                if lang == "EN":
                    if shifted_index > 25:
                        shifted_index -= 26
                elif lang == "AR":
                    if shifted_index > 27:
                        shifted_index -= 28
                cypher_text += alphabets[lang]["letters"][shifted_index]
        return {"status": 200, "cypher_text": cypher_text}
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
    if chars[0] in alphabets[lang]["letters"] or chars[0] in alphabets["AR"]["numbers"] or chars[0] in alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += '/'
            elif char == '.':  # handles end of sentence
                cypher_text += '//'
            # removes special characters
            elif char in alphabets["SpecialCharacters"]:
                pass
            elif (
                char in alphabets["AR"]["numbers"]
                or char in alphabets["EN"]["numbers"]
            ):  # handles numbers
                if char in alphabets["AR"]["numbers"]:
                    cypher_text += ' ' + \
                        alphabets['Morse']['Numbers'][alphabets['AR']["numbers"].index(
                            char)]
                elif char in alphabets["EN"]["numbers"]:
                    cypher_text += ' ' + \
                        alphabets['Morse']['Numbers'][alphabets['EN']["numbers"].index(
                            char)]
            else:
                cypher_text += ' ' + \
                    alphabets['Morse'][lang][alphabets[lang]["letters"].index(
                        char)]
        return {"status": 200, "cypher_text": cypher_text}
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
    if chars[0] in alphabets[lang]["letters"] or chars[0] in alphabets["AR"]["numbers"] or chars[0] in alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += '/'
            elif char == '.':  # handles end of sentence
                cypher_text += '//'
            # removes special characters
            elif char in alphabets["SpecialCharacters"]:
                pass
            elif (
                    char in alphabets["AR"]["numbers"]
                    or char in alphabets["EN"]["numbers"]):
                pass
            else:
                number = alphabets[lang]["letters"].index(char)+1
                cypher_text += ' ' + str(number)
        return {"status": 200, "cypher_text": cypher_text}
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
    if chars[0] in alphabets[lang]["letters"] or chars[0] in alphabets["AR"]["numbers"] or chars[0] in alphabets["EN"]["numbers"]:
        for char in chars:
            if char == " ":  # handles empty space
                cypher_text += '/'
            elif char == '.':  # handles end of sentence
                cypher_text += '//'
            # removes special characters
            elif char in alphabets["SpecialCharacters"]:
                pass
            elif (
                    char in alphabets["AR"]["numbers"]
                    or char in alphabets["EN"]["numbers"]):
                pass
            else:
                number = alphabets[lang]["reverseLetters"].index(
                    char)+1
                cypher_text += ' ' + str(number)
        return {"status": 200, "cypher_text": cypher_text}
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
    if chars[0] in alphabets['EN']["letters"] or chars[0] in alphabets["EN"]["numbers"]:
        for char in chars:
            if char in alphabets["EN"]["numbers"]:
                code = alphabets['NATONumbers'][alphabets['EN']
                                                ["numbers"].index(char)]
                cypher_text += ' ' + str(code)
            elif char == ' ':
                cypher_text += ' (space)'
            elif char in alphabets["SpecialCharacters"]:
                pass
            else:
                code = alphabets['NATOLetters'][alphabets['EN']
                                                ["letters"].index(char)]
                cypher_text += ' ' + str(code)
        return {"status": 200, "cypher_text": cypher_text.strip()}
    else:
        return {"status": 400, "msg": "This method only supports English characters"}


######
### Lookups###
alphabets = {
    "AR": {
        "letters": [
            "ا",
            "ب",
            "ت",
            "ث",
            "ج",
            "ح",
            "خ",
            "د",
            "ذ",
            "ر",
            "ز",
            "س",
            "ش",
            "ص",
            "ض",
            "ط",
            "ظ",
            "ع",
            "غ",
            "ف",
            "ق",
            "ك",
            "ل",
            "م",
            "ن",
            "ه",
            "و",
            "ي",
        ],
        "reverseLetters": [
            "ي",
            "و",
            "ه",
            "ن",
            "م",
            "ل",
            "ك",
            "ق",
            "ف",
            "غ",
            "ع",
            "ظ",
            "ط",
            "ض",
            "ص",
            "ش",
            "س",
            "ز",
            "ر",
            "ذ",
            "د",
            "خ",
            "ح",
            "ج",
            "ث",
            "ت",
            "ب",
            "ا",
        ],
        "numbers": ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"],
    },
    "EN": {
        "letters": [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ],
        "reverseLetters": [
            "Z",
            "Y",
            "X",
            "W",
            "V",
            "U",
            "T",
            "S",
            "R",
            "Q",
            "P",
            "O",
            "N",
            "M",
            "L",
            "K",
            "J",
            "I",
            "H",
            "G",
            "F",
            "E",
            "D",
            "C",
            "B",
            "A",
        ],
        "numbers": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    },
    "Morse": {
        "AR": [
            ".",
            ".-",
            "-...",
            "-",
            "-.-.",
            ".---",
            "....",
            "---",
            "-..",
            "--..",
            ".-.",
            "---.",
            "...",
            "----",
            "-..-",
            "...-",
            "..-",
            "-.--",
            ".-.-",
            "--.",
            "..-.",
            "--.-",
            "-.-",
            ".-..",
            "--",
            "-.",
            "..-..",
            ".--",
            "..",
        ],
        "EN": [
            ".-",
            "-...",
            "-.-.",
            "-..",
            ".",
            "..-.",
            "--.",
            "....",
            "..",
            ".---",
            "-.-",
            ".-..",
            "--",
            "-.",
            "---",
            ".--.",
            "--.-",
            ".-.",
            "...",
            "-",
            "..-",
            "...-",
            ".--",
            "-..-",
            "-.--",
            "--..",
        ],
        "Numbers": [
            ".----",
            "..---",
            "...--",
            "....-",
            ".....",
            "-....",
            "--...",
            "---..",
            "----.",
            "-----",
        ],
    },
    "SpecialCharacters": [
        ".",
        ",",
        "!",
        "?",
        "$",
        "#",
        ";",
        "%",
        "&",
        "*",
        "،",
        ":",
        ")",
        "(",
        " ّ",
        "◌ّ",
    ],
    "NATOLetters": [
        'alpha',
        'bravo',
        'charlie',
        'delta',
        'echo',
        'foxtrot',
        'golf',
        'hotel',
        'india',
        'juliett',
        'kilo',
        'lima',
        'mike',
        'november',
        'oscar',
        'papa',
        'quebec',
        'romeo',
        'sierra',
        'tango',
        'uniform',
        'victor',
        'whiskey',
        'x-ray',
        'yankee',
        'zulu'],
    "NATONumbers": [
        'zero',
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine'
    ]
}
