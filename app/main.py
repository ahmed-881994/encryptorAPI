from fastapi import FastAPI, HTTPException, responses
from . import schemas, methods


app = FastAPI()

def get_application() -> FastAPI:
    application = FastAPI(title="Encryptor", description="Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.",version="0.1.0")
    return application

app = get_application()

@app.get("/",include_in_schema=False)
async def health_check():
    """Used to check the status of the app

    Returns:
        JSON: Current status
    """
    return {"Status": "running"}

@app.get("/favicon.ico", include_in_schema=False)
async def getfavicon():
    return responses.FileResponse('app/assets/favicon.ico')

@app.post("/caesar", response_model= schemas.EncryptRs)
async def caesar(body: schemas.EncryptCaesarRq):
    """Takes input & validates against schema then encrypts using Caesar encryption & returns result

    Args:
        body (schemas.EncryptCaesarRq): Input JSON request

    Raises:
        HTTPException: Error in execution
    Returns:
        JSON: Encrypted text
    """
    result = methods.encrypt_caesar(body.plainText, body.language, body.shift)
    print(result)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[{'msg':result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}

@app.post("/morse", response_model= schemas.EncryptRs)
async def morse(body: schemas.EncryptRq):
    """Takes input & validates against schema then encrypts using Morse encryption & returns result

    Args:
        body (schemas.EncryptRq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = methods.encrypt_morse(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[{'msg':result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}

@app.post("/numeric", response_model= schemas.EncryptRs)
async def numeric(body: schemas.EncryptRq):
    """Takes input & validates against schema then encrypts using Numeric encryption & returns result

    Args:
        body (schemas.EncryptRq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = methods.encrypt_numeric(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[{'msg':result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}

@app.post("/reversenumeric", response_model= schemas.EncryptRs)
async def reverse_numeric(body: schemas.EncryptRq):
    """Takes input & validates against schema then encrypts using Inverse Numeric encryption & returns result

    Args:
        body (schemas.EncryptRq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = methods.encrypt_reverse_numeric(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[{'msg':result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}
    