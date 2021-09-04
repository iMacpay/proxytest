import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from loguru import logger
from datetime import datetime
import time

app = FastAPI()

lock = asyncio.Lock()
counter = 0
proxies = {}


@app.head("/")
def home():
    return ""


@app.get("/")
def home(request: Request):
    global counter, proxies
    ip = request.client.host
    if ip not in proxies:
        proxies[ip] = 0
    proxies[ip] += 1
    counter += 1
    return "OK"


@app.get("/status")
async def stauts():
    global counter, proxies
    async with lock:
        return {
            'counter': counter,
            "ips": len(proxies),
            "detail": proxies,
            "time": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),
        }


@app.get("/reset")
async def reset():
    global counter, proxies
    async with lock:
        counter = 0
        proxies = {}
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app='run:app', host="127.0.0.1", port=8000, log_level="info")
