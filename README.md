# Encryptor
Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.

Available methods:

  * Caesar
  * Morse
  * Numeric
  * Inverse Numeric
  * NATO alphabet
---
## Version: 1.0.3

### /caesar

#### POST
##### Summary:

Encrypts plain text using the Caesar method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded|

### /morse

#### POST
##### Summary:

Encrypts plain text using the Morse method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded|

### /numeric

#### POST
##### Summary:

Encrypts plain text using the Numeric method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded|

### /reversenumeric

#### POST
##### Summary:

Encrypts plain text using the Reverse Numeric method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded|

### /natoalphabet

#### POST
##### Summary:

Encodes plain text using the NATO alphabet method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded|

      
----
## Installing dependencies

To install dependencies please make sure you have Python installed and use

`pip install -r requirements.txt`

to install **FastAPI** and all it's dependencies

---
## Running the app using Uvicorn

run `uvicorn main:app --reload` the `--reload` flag enables hot reload on saving any changes

---
## Docker

- To use the API in docker using the Dockerfile
  1. run `docker build -t encryptorapi .` to build the image
  2. run `docker run -it --rm --name encryptorapi -p 8000:8000  encryptorapi` to start a container with the address `127.0.0.1:8000`

- To use docker-compose

  run `docker-compose up` to spin up a stack of an NGINX server and the API.