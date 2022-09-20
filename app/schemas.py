from enum import Enum
from pydantic import BaseModel, Field

class langEnum(str, Enum):
    AR = 'AR'
    EN = 'EN'
    
class EncryptRq(BaseModel):
    plainText: str = Field(min_length=1)
    language: langEnum
    
class EncryptCaesarRq(EncryptRq):
    shift: int

class EncryptRs(BaseModel):
    cypherText: str