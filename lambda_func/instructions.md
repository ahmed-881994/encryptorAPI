# Deploying FastAPI to AWS Lambda

We'll need to modify the API so that it has a Lambda handler. Use Mangum:

```python
from mangum import Mangum
app = FastAPI()
handler = Mangum(app)
```

We'll also need to install the dependencies into a local directory so we can zip it up.

```bash
pip install -t lib -r requirements.txt
```

We now need to zip it up.

```bash
(cd lib; zip ../lambda_function.zip -r .)
```

Now add our FastAPI file and the JSON file.

```bash
(cd ..; zip lambda_function.zip -u main.py)
```