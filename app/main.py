from unittest import result
from fastapi import Body, FastAPI, HTTPException, status, responses
from . import schemas, methods


app = FastAPI()

def get_application() -> FastAPI:
    application = FastAPI(title="Encryptor", description="Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.",version="0.1.0")
    return application

app = get_application()

@app.get("/",include_in_schema=False)
async def healthCheck():
    return {"Hello": "World"}

@app.get("/favicon.ico", include_in_schema=False)
async def getfavicon():
    return responses.FileResponse('app/assets/favicon.ico')

@app.post("/caesar", response_model= schemas.EncryptRs)
async def caesar(body: schemas.EncryptCaesarRq):
    result = methods.encryptCaesar(body.plainText, body.language, body.shift)
    print(result)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=result['detail'])  
    else:
        return {"cypherText": result['cypherText']}

@app.post("/morse", response_model= schemas.EncryptRs)
async def morse(body: schemas.EncryptRq):
    result = methods.encryptMorse(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return {"cypherText": result['cypherText']}

@app.post("/numeric", response_model= schemas.EncryptRs)
async def numeric(body: schemas.EncryptRq):
    result = methods.encryptNumeric(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return {"cypherText": result['cypherText']}

@app.post("/reversenumeric", response_model= schemas.EncryptRs)
async def reversenumeric(body: schemas.EncryptRq):
    result = methods.encryptReverseNumeric(body.plainText, body.language)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return {"cypherText": result['cypherText']}