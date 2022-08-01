from fastapi import Body, FastAPI, status
from . import schemas


app = FastAPI()




@app.get("/")
async def healthCheck():
    return {"Hello": "World"}

@app.post("/caesar", response_model= schemas.EncryptRs)
async def caesar(body: schemas.EncryptCaesarRq):
    return {'cypherText':'test'}

@app.post("/morse")
async def morse(body: schemas.EncryptRq):
    return body

@app.post("/numeric")
async def numeric(body: schemas.EncryptRq):
    return body

@app.post("/reversenumeric")
async def reversenumeric(body: schemas.EncryptRq):
    return body