# start by pulling the python image
FROM python:latest

# switch working directory
WORKDIR /code

# copy the requirements file into the image
COPY ./requirements.txt ./requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy every content from the local file to the image
COPY ./app ./app

EXPOSE 8000

ENTRYPOINT [ "uvicorn" ]

CMD ["main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# docker build -t encryptorapi .
# docker run -it --rm --name encryptorapi -p 8000:8000  encryptorapi