import re
from fastapi import Request
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from perlin_gener import map_fin
from squares import generate_map
from xoring import generate_xor
from graphic import create_terrain

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

type_of = 0
n_of_cunks = 0
length_of_chunk = 0
height = 0

@app.get("/")
async def home():
    return FileResponse("static/html/div.html")

@app.post('/')
async def get_info(request: Request):
    global type_of 
    type_of = int(request.headers.get('type_of_generation'))
    global n_of_cunks
    n_of_cunks = int(request.headers.get('chunks'))
    global height
    height = int(request.headers.get('height'))
    global length_of_chunk
    length_of_chunk = int(request.headers.get('length'))


@app.get("/generated", response_class=HTMLResponse)
async def create():
    global type_of, n_of_cunks, length_of_chunk, height
    match type_of:
        case 1:
            return HTMLResponse(create_terrain(map_fin(n_of_cunks, length_of_chunk, height)))
        case 2:
            return HTMLResponse(create_terrain(generate_xor(n_of_cunks, length_of_chunk, height)))
        case 3:
            return HTMLResponse(create_terrain(generate_map(n_of_cunks, 2**length_of_chunk+1, height)))



if __name__ == '__main__':
    uvicorn.run('app:app', port=8000, reload=True)