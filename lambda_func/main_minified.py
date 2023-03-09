_m='.--'
_l='.-..'
_k='-.-'
_j='--.-'
_i='..-.'
_h='--.'
_g='-.--'
_f='..-'
_e='...-'
_d='-..-'
_c='...'
_b='.-.'
_a='--..'
_Z='-..'
_Y='---'
_X='....'
_W='.---'
_V='-.-.'
_U='-...'
_T='NATOLetters'
_S='NATONumbers'
_R=False
_Q='reverseLetters'
_P='Numbers'
_O='//'
_N='Morse'
_M="Plain text and language choice don't match"
_L='/'
_K='SpecialCharacters'
_J='cypherText'
_I='.'
_H='cypher_text'
_G='letters'
_F=' '
_E='msg'
_D='AR'
_C='EN'
_B='status'
_A='numbers'
from fastapi import FastAPI,HTTPException,Request,status
from fastapi.responses import JSONResponse,FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from mangum import Mangum
from enum import Enum
from typing import Dict,List
from pydantic import BaseModel,Field
class lang_enum(str,Enum):AR=_D;EN=_C
class EncryptRq(BaseModel):plainText:str=Field(min_length=1);language:lang_enum
class EncryptNATORq(BaseModel):plainText:str=Field(min_length=1)
class EncryptCaesarRq(EncryptRq):shift:int
class EncryptRs(BaseModel):cypherText:str
class Detail(BaseModel):msg:str
class ErrorRs(BaseModel):detail:List[Detail]
async def rate_limit_exceeded_handler(request:Request,exc:RateLimitExceeded):A=[];A.append({_E:f"Rate limit exceeded: {exc.detail} Try again in a while..."});B={'detail':A};return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS,content=B)
def get_application()->FastAPI:B='model';A=FastAPI(responses={429:{B:ErrorRs},400:{B:ErrorRs}},exception_handlers={429:rate_limit_exceeded_handler},title='Encryptor',description='Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.',version='0.1.0');return A
app=get_application()
LIMIT='5/minute'
handler=Mangum(app)
limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,rate_limit_exceeded_handler)
@app.get(_L,include_in_schema=_R)
async def health_check():return{'Status':'running'}
@app.get('/favicon.ico',include_in_schema=_R)
async def get_favicon():return FileResponse('app/assets/favicon.ico')
@app.post('/caesar',response_model=EncryptRs)
@limiter.limit(LIMIT)
async def caesar(body:EncryptCaesarRq,request:Request):
	B=body;A=encrypt_caesar(B.plainText,B.language,B.shift)
	if A[_B]!=200:raise HTTPException(status_code=A[_B],detail=[{_E:A[_E]}])
	else:return{_J:A[_H]}
@app.post('/morse',response_model=EncryptRs)
@limiter.limit(LIMIT)
async def morse(body:EncryptRq,request:Request):
	A=encrypt_morse(body.plainText,body.language)
	if A[_B]!=200:raise HTTPException(status_code=A[_B],detail=[{_E:A[_E]}])
	else:return{_J:A[_H]}
@app.post('/numeric',response_model=EncryptRs)
@limiter.limit(LIMIT)
async def numeric(body:EncryptRq,request:Request):
	A=encrypt_numeric(body.plainText,body.language)
	if A[_B]!=200:raise HTTPException(status_code=A[_B],detail=[{_E:A[_E]}])
	else:return{_J:A[_H]}
@app.post('/reversenumeric',response_model=EncryptRs)
@limiter.limit(LIMIT)
async def reverse_numeric(body:EncryptRq,request:Request):
	A=encrypt_reverse_numeric(body.plainText,body.language)
	if A[_B]!=200:raise HTTPException(status_code=A[_B],detail=[{_E:A[_E]}])
	else:return{_J:A[_H]}
@app.post('/natoalphabet',response_model=EncryptRs)
@limiter.limit(LIMIT)
async def nato_alphabet(body:EncryptNATORq,request:Request):
	A=encode_NATO(body.plainText)
	if A[_B]!=200:raise HTTPException(status_code=A[_B],detail=[{_E:A[_E]}])
	else:return{_J:A[_H]}
def handle_arabic_variants(chars:list[str])->list[str]:
	A=chars
	for B in A:
		if B in['أ','ء','ئ','ى','آ','إ']:A[A.index(B)]='ا'
		elif B=='ة':A[A.index(B)]='ت'
		elif B=='ؤ':A[A.index(B)]='و'
	return A
def encrypt_caesar(plain_text:str,lang:str,shift:int)->Dict:
	F=plain_text;A=lang;E='';F=F.upper();B=list(F)
	if A==_D:B=handle_arabic_variants(B)
	if B[0]in alphabets[A][_G]or B[0]in alphabets[_D][_A]or B[0]in alphabets[_C][_A]:
		for C in B:
			if C==_F:E+=_F
			elif C in alphabets[_D][_A]or C in alphabets[_C][_A]:E+=C
			elif C in alphabets[_K]:0
			else:
				D=alphabets[A][_G].index(C)+shift
				if A==_C:
					if D>25:D-=26
				elif A==_D:
					if D>27:D-=28
				E+=alphabets[A][_G][D]
		return{_B:200,_H:E}
	else:return{_B:400,_E:_M}
def encrypt_morse(plain_text:str,lang:str)->Dict:
	E=plain_text;D=lang;B='';E=E.upper();C=list(E)
	if D==_D:C=handle_arabic_variants(C)
	if C[0]in alphabets[D][_G]or C[0]in alphabets[_D][_A]or C[0]in alphabets[_C][_A]:
		for A in C:
			if A==_F:B+=_L
			elif A==_I:B+=_O
			elif A in alphabets[_K]:0
			elif A in alphabets[_D][_A]or A in alphabets[_C][_A]:
				if A in alphabets[_D][_A]:B+=_F+alphabets[_N][_P][alphabets[_D][_A].index(A)]
				elif A in alphabets[_C][_A]:B+=_F+alphabets[_N][_P][alphabets[_C][_A].index(A)]
			else:B+=_F+alphabets[_N][D][alphabets[D][_G].index(A)]
		return{_B:200,_H:B}
	else:return{_B:400,_E:_M}
def encrypt_numeric(plain_text:str,lang:str)->Dict:
	E=lang;D=plain_text;C='';D=D.upper();A=list(D)
	if E==_D:A=handle_arabic_variants(A)
	if A[0]in alphabets[E][_G]or A[0]in alphabets[_D][_A]or A[0]in alphabets[_C][_A]:
		for B in A:
			if B==_F:C+=_L
			elif B==_I:C+=_O
			elif B in alphabets[_K]:0
			elif B in alphabets[_D][_A]or B in alphabets[_C][_A]:0
			else:F=alphabets[E][_G].index(B)+1;C+=_F+str(F)
		return{_B:200,_H:C}
	else:return{_B:400,_E:_M}
def encrypt_reverse_numeric(plain_text:str,lang:str)->Dict:
	E=lang;D=plain_text;C='';D=D.upper();A=list(D)
	if E==_D:A=handle_arabic_variants(A)
	if A[0]in alphabets[E][_G]or A[0]in alphabets[_D][_A]or A[0]in alphabets[_C][_A]:
		for B in A:
			if B==_F:C+=_L
			elif B==_I:C+=_O
			elif B in alphabets[_K]:0
			elif B in alphabets[_D][_A]or B in alphabets[_C][_A]:0
			else:F=alphabets[E][_Q].index(B)+1;C+=_F+str(F)
		return{_B:200,_H:C}
	else:return{_B:400,_E:_M}
def encode_NATO(plain_text:str)->Dict:
	C=plain_text;A='';C=C.upper();D=list(C)
	if D[0]in alphabets[_C][_G]or D[0]in alphabets[_C][_A]:
		for B in D:
			if B in alphabets[_C][_A]:E=alphabets[_S][alphabets[_C][_A].index(B)];A+=_F+str(E)
			elif B==_F:A+=' (space)'
			else:E=alphabets[_T][alphabets[_C][_G].index(B)];A+=_F+str(E)
		return{_B:200,_H:A.strip()}
	else:return{_B:400,_E:'This method only supports English characters'}
alphabets={_D:{_G:['ا','ب','ت','ث','ج','ح','خ','د','ذ','ر','ز','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ك','ل','م','ن','ه','و','ي'],_Q:['ي','و','ه','ن','م','ل','ك','ق','ف','غ','ع','ظ','ط','ض','ص','ش','س','ز','ر','ذ','د','خ','ح','ج','ث','ت','ب','ا'],_A:['٠','١','٢','٣','٤','٥','٦','٧','٨','٩']},_C:{_G:['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],_Q:['Z','Y','X','W','V','U','T','S','R','Q','P','O','N','M','L','K','J','I','H','G','F','E','D','C','B','A'],_A:['0','1','2','3','4','5','6','7','8','9']},_N:{_D:[_I,'.-',_U,'-',_V,_W,_X,_Y,_Z,_a,_b,'---.',_c,'----',_d,_e,_f,_g,'.-.-',_h,_i,_j,_k,_l,'--','-.','..-..',_m,'..'],_C:['.-',_U,_V,_Z,_I,_i,_h,_X,'..',_W,_k,_l,'--','-.',_Y,'.--.',_j,_b,_c,'-',_f,_e,_m,_d,_g,_a],_P:['.----','..---','...--','....-','.....','-....','--...','---..','----.','-----']},_K:[_I,',','!','?','$','#',';','%','&','*','،',':',')','(',' ّ','◌ّ'],_T:['alpha','bravo','charlie','delta','echo','foxtrot','golf','hotel','india','juliett','kilo','lima','mike','november','oscar','papa','quebec','romeo','sierra','tango','uniform','victor','whiskey','x-ray','yankee','zulu'],_S:['zero','one','two','three','four','five','six','seven','eight','nine']}