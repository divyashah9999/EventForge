# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

# Ensure the generated_decks directory exists
GENERATED_DIR = os.path.join(os.getcwd(), "generated_decks")
if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)

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
    prompt: str = ""
    vision: str = ""

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
    try:
        # Use whichever one is provided
        prompt_to_use = req.prompt if req.prompt else req.vision
        if not prompt_to_use:
            raise ValueError("No prompt or vision provided in request.")

        event_json = generate_event_data(prompt_to_use)
        workspace_url = create_event_workspace(event_json)
        pptx_path = generate_pitch_deck(event_json)

        # Move the file to the dedicated directory
        final_filename = os.path.basename(pptx_path)
        final_path = os.path.join(GENERATED_DIR, final_filename)
        shutil.move(pptx_path, final_path)

        return {
            "status": "success",
            "workspace_url": workspace_url,
            "pptx_filename": final_filename,
            "event_data": event_json
        }
    except Exception as e:
        print(f"❌ SERVER ERROR: {str(e)}")
        error_msg = str(e)
        if "429" in error_msg or "Quota" in error_msg:
            friendly_msg = "Google API Rate Limit reached (Free Tier). Please wait 30-40 seconds and click Generate again!"
        else:
            friendly_msg = f"Generation failed: {error_msg}"
            
        return {
            "status": "error", 
            "message": friendly_msg
        }

@app.get("/download/{filename}")
def download_pptx(filename: str):
    path = os.path.join(GENERATED_DIR, filename)
    if not os.path.exists(path):
        return {"error": "File not found"}
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=filename
    )