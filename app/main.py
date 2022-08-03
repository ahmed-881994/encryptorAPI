from unittest import result
from fastapi import Body, FastAPI, HTTPException, status
from . import schemas, methods


app = FastAPI()

def get_application() -> FastAPI:
    application = FastAPI(title="Encryptor", description="Encrypt plain text using simple encryption i.e: Caesar, Morse,..., etc.",version="0.1.0")
    # origins = [
    #     config.API_CONFIG["origin_local_ip"],
    #     config.API_CONFIG["origin_local_url"]
    # ]
    # application.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    #application.include_router(processA.router)
    return application

app = get_application()

@app.get("/")
async def healthCheck():
    return {"Hello": "World"}

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

@app.post("/numeric")
async def numeric(body: schemas.EncryptRq):
    return body

@app.post("/reversenumeric")
async def reversenumeric(body: schemas.EncryptRq):
    return body