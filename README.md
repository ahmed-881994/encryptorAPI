# Encryptor
Encrypt plain text using simple encryption *i.e*: ***Caesar***, ***Morse***, etc.

Available methods:

  * Caesar
  * Morse
  * Numeric
  * Inverse Numeric
---
## Version: 0.1.0

### /caesar

#### POST
##### Summary:

Encrypts plain text using the Caesar method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /morse

#### POST
##### Summary:

Encrypts plain text using the Morse method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /numeric

#### POST
##### Summary:

Encrypts plain text using the Numeric method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /reversenumeric

#### POST
##### Summary:

Encrypts plain text using the Reverse Numeric method

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

      
----
      
To install dependencies please make sure you have Python installed and use

`$ pip install fastapi[all]`

to install **FastAPI** and all it's dependencies
