import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routers import date

app = FastAPI()
app.title = "Backend EMT"
app.version = '1.0.0'

app.include_router(date.route_date)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:9000",
    # Esta tiene que ser donde se inicia fast api
    # 'http://192.168.173.242:8080'
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=['Bienvenido'])
def welcome():
    return HTMLResponse('<h2> Api EMT</h2>')

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
