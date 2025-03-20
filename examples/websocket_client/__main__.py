import uvicorn
from .websocket_client import app
uvicorn.run("__main__:app", port=8001, log_level="info")
