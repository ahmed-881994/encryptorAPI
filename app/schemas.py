from enum import Enum

from pydantic import BaseModel, Field

class lang_enum(str, Enum):

    AR = 'AR'

    EN = 'EN'
class EncryptRq(BaseModel):

    plainText: str = Field(min_length=1)
    language: lang_enum
    

class EncryptCaesarRq(EncryptRq):

    shift: int


class EncryptRs(BaseModel):

    cypherText: str
    