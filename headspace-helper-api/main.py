from fastapi import FastAPI

app = FastAPI(title='headspace helper api')


@app.get('/')
def index():
    return {'headspace-helper-api': 'initiated'}
