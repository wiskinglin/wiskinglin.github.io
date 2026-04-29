import asyncio
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import edge_tts
from typing import AsyncGenerator

app = FastAPI()

# Mount static files for audio
os.makedirs("audio_chunks", exist_ok=True)
app.mount("/audio_chunks", StaticFiles(directory="audio_chunks"), name="audio_chunks")

class GenerateRequest(BaseModel):
    prompt: str

async def generate_speech_chunk(text_chunk: str, chunk_index: int, output_dir: str = "audio_chunks"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    voice = "zh-TW-HsiaoChenNeural"
    output_file = os.path.join(output_dir, f"chunk_{chunk_index}.mp3")
    
    try:
        communicate = edge_tts.Communicate(text_chunk, voice, rate="+0%")
        await communicate.save(output_file)
        # Using forward slashes for URLs
        return f"audio_chunks/chunk_{chunk_index}.mp3"
    except Exception as e:
        print(f"Error generating speech chunk {chunk_index}: {e}")
        return None

class TTSRequest(BaseModel):
    text: str
    index: int

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    audio_file = await generate_speech_chunk(request.text, request.index)
    if audio_file:
        return {"url": f"/{audio_file}"}
    return {"error": "Failed to generate audio"}

@app.get("/")
async def get_index():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
