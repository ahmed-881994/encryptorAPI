from pydantic import BaseModel

class EncryptRq(BaseModel):
    plainText: str
    language: str
    
class EncryptCaesarRq(EncryptRq):
    shift: int

class EncryptRs(BaseModel):
    cypherText: str