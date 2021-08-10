from fastapi import FastAPI
from uvicorn import run as uvicorn_run


ceviche = FastAPI()


if __name__ == "__main__":

    uvicorn_run("main:ceviche", host="0.0.0.0", port=8000, log_level="debug")
