import os
import json
import google.generativeai as genai
from google.generativeai.types import content_types
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the exact JSON schema we want the model to output
# Using the OpenAPI 3.0 schema format required by Gemini
response_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The official name of the event."
        },
        "brief": {
            "type": "string",
            "description": "A short 2-3 sentence description of the event's purpose and goals."
        },
        "tasks": {
            "type": "array",
            "description": "A list of 5-8 actionable tasks needed to execute this event.",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Clear, actionable task name."
                    },
                    "department": {
                        "type": "string",
                        "description": "The team responsible.",
                        "enum": ["PR & Media", "Logistics", "Tech", "Design"]
                    },
                    "status": {
                        "type": "string",
                        "description": "Initial task status.",
                        "enum": ["Not Started", "In Progress", "Done"]
                    }
                },
                "required": ["name", "department", "status"]
            }
        },
        "pr_plan": {
            "type": "object",
            "description": "Comprehensive PR and marketing plan.",
            "properties": {
                "social_calendar": {
                    "type": "array",
                    "description": "List of specific social media posts (e.g. LinkedIn, Twitter copy).",
                    "items": {"type": "string"}
                },
                "influencer_outreach": {
                    "type": "array",
                    "description": "List of strategies or targets for influencer outreach.",
                    "items": {"type": "string"}
                },
                "email_template": {
                    "type": "string",
                    "description": "A complete email template for event promotion."
                }
            },
            "required": ["social_calendar", "influencer_outreach", "email_template"]
        },
        "logistics_plan": {
            "type": "object",
            "description": "Comprehensive logistics and operations plan.",
            "properties": {
                "budget_table": {
                    "type": "string",
                    "description": "A budget breakdown formatted strictly as a Markdown table."
                },
                "hardware_checklist": {
                    "type": "array",
                    "description": "List of required hardware and AV equipment.",
                    "items": {"type": "string"}
                },
                "venue_setup": {
                    "type": "string",
                    "description": "Detailed description of the venue layout and setup requirements."
                }
            },
            "required": ["budget_table", "hardware_checklist", "venue_setup"]
        },
        "color_palette": {
            "type": "array",
            "description": "A list of exactly 3 hex color codes for the event brand: [primary, accent, text]. Example: ['#1A1A2E', '#7C3AED', '#FFFFFF']",
            "items": {"type": "string"}
        },
        "pitch_deck": {
            "type": "array",
            "description": "Exactly 7 slides for the event pitch deck, in order.",
            "items": {
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide position, 1-7."
                    },
                    "title": {
                        "type": "string",
                        "description": "Slide title."
                    },
                    "content": {
                        "type": "string",
                        "description": "Full body text for the slide. Use newlines for bullet points."
                    },
                    "visual_guidance": {
                        "type": "string",
                        "description": "Short designer note describing the visual/layout intent for this slide."
                    }
                },
                "required": ["slide_number", "title", "content", "visual_guidance"]
            }
        }
    },
    "required": ["title", "brief", "tasks", "pr_plan", "logistics_plan", "color_palette", "pitch_deck"]
}

# Initialize the model with the system instruction
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="You are a high-level Event COO. Your goal is to provide granular, actionable plans. For the budget, use a markdown table format. For PR, provide specific copy for LinkedIn and Twitter. Output: Structured JSON for Notion. Do not include conversational text outside of the JSON structure.",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
        temperature=0.7,
    )
)

def generate_event_data(prompt: str) -> dict:
    """
    Calls Gemini to generate structured event planning data based on the user's prompt.
    Returns the parsed JSON dictionary.
    """
    print(f"🧠 Asking Gemini to plan: '{prompt}'...")
    response = model.generate_content(prompt)
    
    # The response is guaranteed to be a JSON string that matches our schema
    try:
        data = json.loads(response.text)
        print("✅ Received structured JSON from Gemini!")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON from Gemini: {e}")
        print(f"Raw response: {response.text}")
        raise

def generate_poster_concepts(prompt: str) -> list:
    """Returns 3 poster vibe concepts for the user to choose from."""
    
    system_prompt = """
You are a creative director for events. Given an event description, generate exactly 3 distinct poster vibe concepts.

Return ONLY valid JSON — no markdown fences, no explanation. This exact structure:

[
  {
    "vibe_id": "vibe_1",
    "vibe_name": "Short evocative name (2-3 words)",
    "mood": "One sentence describing the feeling",
    "color_palette": {
      "primary": "#hex",
      "secondary": "#hex", 
      "accent": "#hex",
      "background": "#hex",
      "text": "#hex"
    },
    "typography_feel": "e.g. Bold geometric sans-serif, elegant serif, hand-crafted",
    "visual_elements": ["element1", "element2", "element3"],
    "poster_description": "2-3 sentences describing what the poster looks like in detail",
    "best_for": "Who this vibe appeals to"
  }
]

Rules:
- 3 concepts only, each genuinely different in mood and palette
- No neon colors. No electric blue. No purple gradients. No AI-robot aesthetics.
- Warm earth tones, organic palettes, premium human-made feel
- Palettes: think deep charcoal + cream, terracotta + sage, midnight navy + warm gold
- vibe_names should feel like creative directions: e.g. "Raw & Underground", "Warm & Collegiate", "Crisp & Corporate"
- visual_elements: 3 concrete design motifs (e.g. "halftone texture", "geometric grid lines", "hand-drawn borders")
"""

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )
    
    full_prompt = f"{system_prompt}\n\nEvent description: {prompt}"
    response = model.generate_content(full_prompt)
    concepts = json.loads(response.text)
    
    # Safety: ensure exactly 3
    return concepts[:3]


def generate_brand_identity(event_data: dict, chosen_vibe: dict) -> dict:
    """Takes chosen vibe + event data, returns brand identity description."""
    
    system_prompt = """
You are a brand strategist. Given an event's data and a chosen visual vibe, write a structured brand identity.

Return ONLY valid JSON — no markdown fences, no explanation:

{
  "brand_name": "Short punchy event brand name or tagline",
  "theme_statement": "1 sentence: the core idea of this event's identity",
  "visual_identity": "2-3 sentences describing colors, typography, and design feel for any designer or AI agent",
  "tone_of_voice": "2-3 sentences: how all communication should sound — formal/casual, energetic/calm, etc.",
  "target_audience": "1-2 sentences on who this brand speaks to",
  "ai_agent_brief": "A single paragraph (5-7 sentences) that any AI agent (image generator, copywriter, social media bot) can read to understand and maintain this brand's identity across all outputs. Be specific about colors, mood, typography, and communication style.",
  "do_list": ["3 brand dos"],
  "dont_list": ["3 brand don'ts"]
}
"""

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )

    full_prompt = f"""{system_prompt}

Event data:
Title: {event_data.get('title')}
Brief: {event_data.get('brief')}

Chosen vibe:
Name: {chosen_vibe.get('vibe_name')}
Mood: {chosen_vibe.get('mood')}
Colors: {json.dumps(chosen_vibe.get('color_palette'))}
Typography: {chosen_vibe.get('typography_feel')}
Visual elements: {chosen_vibe.get('visual_elements')}
"""

    response = model.generate_content(full_prompt)
    return json.loads(response.text)
