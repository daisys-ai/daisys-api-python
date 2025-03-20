import sys, os, asyncio, time, logging, pathlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn

from daisys import DaisysAPI
from daisys.v1.speak import VoiceInfo, HTTPStatusError, Status, TakeResponse

# Override DAISYS_EMAIL and DAISYS_PASSWORD with your details!
EMAIL = os.environ.get('DAISYS_EMAIL', 'user@example.com')
PASSWORD = os.environ.get('DAISYS_PASSWORD', 'pw')

# Please see tokens_example.py for how to use an access token instead of a password.

speak = None
voice: VoiceInfo = None
logger = logging.getLogger('uvicorn.error')

@asynccontextmanager
async def speak_client(app: FastAPI):
    global speak, voice
    async with DaisysAPI('speak', email=EMAIL, password=PASSWORD) as speak:
        logger.info('Found Daisys Speak API %s', await speak.version())
        voices = await speak.get_voices()
        models = ['english-gb-v2.1', 'theatrical-v2']
        voice = [v for v in voices if v.model in models][0]
        logger.info('Found voice %s (%s)', voice.name, voice.voice_id)
        yield

app = FastAPI(lifespan=speak_client)

@app.get("/")
async def index():
    return FileResponse(pathlib.Path(__file__).parent / 'websocket_client.html')

@app.get("/{filename}.js")
async def js(filename: str):
    return FileResponse(pathlib.Path(__file__).parent / f'{filename}.js')

@app.get("/ws_url")
async def ws_url() -> HTMLResponse:
    s = await speak.websocket_url(voice_id=voice.voice_id)
    return HTMLResponse(s)

@app.get("/voice_id")
async def voice_id() -> HTMLResponse:
    return HTMLResponse(voice.voice_id)
