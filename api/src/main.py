from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import route


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


app.include_router(route.router)
