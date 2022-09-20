# start by pulling the python image
FROM python:3

# switch working directory
WORKDIR /code

# copy the requirements file into the image
COPY ./requirements.txt /code/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy every content from the local file to the image
COPY ./app /code/app

# configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t encryptorapi .
# docker run -it --rm --name encryptorapi -p 8000:8000  encryptorapi