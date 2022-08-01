from fastapi import Body, FastAPI, status
from . import schemas


app = FastAPI()




@app.get("/")
async def healthCheck():
    return {"Hello": "World"}

@app.post("/caesar")
async def caesar(body: schemas.EncryptCaesarRq):
    return body

@app.post("/morse")
async def morse(body: schemas.EncryptRq):
    return body

@app.post("/numeric")
async def numeric(body: schemas.EncryptRq):
    return body

@app.post("/reversenumeric")
async def reversenumeric(body: schemas.EncryptRq):
    return body