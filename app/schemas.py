from enum import Enum
from typing import List
from pydantic import BaseModel, Field


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
