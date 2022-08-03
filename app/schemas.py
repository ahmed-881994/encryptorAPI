from enum import Enum
from pydantic import BaseModel

class langEnum(str, Enum):
    AR = 'AR'
    EN = 'EN'
    
class EncryptRq(BaseModel):
    plainText: str
    language: langEnum
    
class EncryptCaesarRq(EncryptRq):
    shift: int

class EncryptRs(BaseModel):
    cypherText: str