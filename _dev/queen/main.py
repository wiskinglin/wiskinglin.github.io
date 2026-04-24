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

# Mock generator simulating Divergence, Convergence, Structuring
async def mock_llm_generator(prompt: str) -> AsyncGenerator[dict, None]:
    # Stage 1: Intro
    yield {"type": "status", "message": "Analyzing prompt: Divergence stage..."}
    await asyncio.sleep(1)
    
    intro_text = f"關於「{prompt}」，我們將進行深入探討。這是一個非常有趣且具備多維度思考的議題。"
    yield {"type": "text", "content": intro_text}
    audio_file = await generate_speech_chunk(intro_text, 0)
    if audio_file:
        yield {"type": "audio", "url": f"/{audio_file}", "index": 0}
        
    # Stage 2: Main points
    yield {"type": "status", "message": "Structuring content: Convergence stage..."}
    await asyncio.sleep(1)
    
    for i in range(1, 4):
        chunk_text = f"第 {i} 部分：探討核心觀點。我們發現這個領域充滿挑戰，但也蘊含巨大機會。這部分需要更深入的研究數據來支持。"
        yield {"type": "text", "content": f"\n\n### {i}. 核心觀點 {i}\n\n" + chunk_text}
        audio_file = await generate_speech_chunk(chunk_text, i)
        if audio_file:
            yield {"type": "audio", "url": f"/{audio_file}", "index": i}
            
    # Stage 3: Conclusion
    yield {"type": "status", "message": "Finalizing conclusion..."}
    await asyncio.sleep(1)
    
    conclusion_text = "總結來說，未來的發展取決於我們如何應用這些知識。謝謝您的聆聽。"
    yield {"type": "text", "content": f"\n\n### 結論\n\n" + conclusion_text}
    audio_file = await generate_speech_chunk(conclusion_text, 4)
    if audio_file:
        yield {"type": "audio", "url": f"/{audio_file}", "index": 4}
        
    yield {"type": "status", "message": "Generation complete."}
    yield {"type": "done"}

@app.get("/generate_stream")
async def generate_stream(prompt: str):
    async def event_generator():
        async for event in mock_llm_generator(prompt):
            yield {"data": json.dumps(event)}
            
    return EventSourceResponse(event_generator())

@app.get("/")
async def get_index():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
