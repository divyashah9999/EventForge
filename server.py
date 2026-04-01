# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

import json
from gemini_agent import generate_event_data, generate_poster_concepts, generate_brand_identity
from notion_agent import create_event_workspace
from pptx_agent import generate_pitch_deck

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

class PosterRequest(BaseModel):
    prompt: str

class BrandRequest(BaseModel):
    event_data: dict
    chosen_vibe: dict

@app.post("/poster-concepts")
def poster_concepts(req: PosterRequest):
    try:
        concepts = generate_poster_concepts(req.prompt)
        return {
            "status": "success",
            "concepts": concepts
        }
    except json.JSONDecodeError:
        return {"status": "error", "message": "Gemini returned invalid JSON for poster concepts"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/brand-identity")
def brand_identity(req: BrandRequest):
    try:
        identity = generate_brand_identity(req.event_data, req.chosen_vibe)
        return {
            "status": "success",
            "brand_identity": identity
        }
    except json.JSONDecodeError:
        return {"status": "error", "message": "Gemini returned invalid JSON for brand identity"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/generate")
def generate(req: PromptRequest):
    event_json = generate_event_data(req.prompt)
    workspace_url = create_event_workspace(event_json)
    pptx_path = generate_pitch_deck(event_json)

    return {
        "status": "success",
        "workspace_url": workspace_url,
        "pptx_filename": os.path.basename(pptx_path),
        "event_data": event_json
    }

@app.get("/download/{filename}")
def download_pptx(filename: str):
    path = os.path.join(os.getcwd(), filename)
    if not os.path.exists(path):
        return {"error": "File not found"}
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=filename
    )