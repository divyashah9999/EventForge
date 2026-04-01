# EventForge: The Ultimate AI Event Branding & Planning Platform

**EventForge** is a comprehensive, end-to-end automation platform designed for modern event organizers. It transforms a single natural language prompt into a fully interactive Notion project workspace, a professional PPTX pitch deck, and a complete brand identity—all in under 30 seconds.

## 🚀 Key Features

*   **Intelligent Logic Trees**: Generates a deep event blueprint (timeline, tasks, budget, and marketing strategy) using Gemini's logic.
*   **Notion Workspace Automation**: Creates a live, shared workspace with structured data across multiple databases.
*   **PPTX Pitch Deck Synthesis**: Automatically exports key event info into a clean 16:9 widescreen presentation deck.
*   **Visual Persona & Brand ID**: Generates 3 unique "Poster Vibes" using custom-curated earth-tone color palettes. Includes a full brand strategy and an AI Agent Brief for further creative collaboration.
*   **Premium Glassmorphism UX**: A high-end, responsive dashboard built with modern CSS and earthy aesthetics.

## 🛠️ Setup Instructions

1.  **Clone & Install**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    Create a `.env` file from the `.env.example` template:
    ```bash
    GEMINI_API_KEY=your_google_key
    NOTION_TOKEN=your_notion_secret_key
    NOTION_MASTER_PAGE_ID=your_shared_page_id
    ```

3.  **Run the Engine**:
    ```bash
    uvicorn server:app --host 0.0.0.0 --port 8000
    ```

4.  **Access the Dashboard**:
    Open `http://localhost:8000/ui/plan_a_new_event/code.html` in your browser.

## 🏗️ Architecture

*   **Backend**: FastAPI (Python)
*   **AI Engine**: Gemini 2.5 Flash
*   **Platform Integrations**: Notion API, Python-PPTX
*   **Frontend**: Vanilla HTML/JS with Material Design Tokens and Modern Glassmorphism CSS.

---
Built for the 2026 AI Innovation Hackathon.
