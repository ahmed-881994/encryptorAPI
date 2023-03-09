from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, FileResponse
from . import schemas, methods
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    detail = []
    detail.append(
        {'msg': f'Rate limit exceeded: {exc.detail} Try again in a while...'})
    res = {'detail': detail}
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=res
    )


def get_application() -> FastAPI:
    application = FastAPI(responses={429: {'model': schemas.ErrorRs}, 400: {'model': schemas.ErrorRs}}, exception_handlers={
                          429: rate_limit_exceeded_handler}, title="Encryptor", description="Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.", version="1.0.3")
    return application


app = get_application()

LIMIT = '5/minute'
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


@app.get("/", include_in_schema=False)
async def health_check():
    """Used to check the status of the app

    Returns:
        JSON: Current status
    """
    return {"Status": "running"}


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse('app/assets/favicon.ico')


@app.post("/caesar", response_model=schemas.EncryptRs)
@limiter.limit(LIMIT)
async def caesar(body: schemas.EncryptCaesarRq, request: Request):
    """Takes input & validates against schema then encrypts using Caesar encryption & returns result

    Args:
        body (schemas.EncryptCaesarRq): Input JSON request

    Raises:
        HTTPException: Error in execution
    Returns:
        JSON: Encrypted text
    """
    result = methods.encrypt_caesar(body.plainText, body.language, body.shift)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/morse", response_model=schemas.EncryptRs)
@limiter.limit(LIMIT)
async def morse(body: schemas.EncryptRq, request: Request):
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
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/numeric", response_model=schemas.EncryptRs)
@limiter.limit(LIMIT)
async def numeric(body: schemas.EncryptRq, request: Request):
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
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/reversenumeric", response_model=schemas.EncryptRs)
@limiter.limit(LIMIT)
async def reverse_numeric(body: schemas.EncryptRq, request: Request):
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
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}


@app.post("/natoalphabet", response_model=schemas.EncryptRs)
@limiter.limit(LIMIT)
async def nato_alphabet(body: schemas.EncryptNATORq, request: Request):
    """Takes input & validates against schema then encodes using NATO alphabet encoding & returns result

    Args:
        body (schemas.EncryptNATORq): Input JSON request

    Raises:
        HTTPException: Error in execution

    Returns:
        JSON: Encrypted text
    """
    result = methods.encode_NATO(body.plainText)
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=[
                            {'msg': result['msg']}])
    else:
        return {"cypherText": result['cypher_text']}
