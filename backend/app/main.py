from fastapi import FastAPI

app = FastAPI(title='Coding Assistant Backend')

@app.get('/')
def root():
    return {'message': 'Backend funcionando!'}
