# EventForge: The Ultimate AI Event Branding & Planning Platform

**EventForge** is a comprehensive, end-to-end automation platform designed for modern event organizers. It transforms a single natural language prompt into a fully interactive Notion project workspace, a professional PPTX pitch deck, and a complete brand identity—all in under 30 seconds.

---

## 💡 The Problem We're Solving
Planning an event is fundamentally broken. Organizers waste hours jumping between ChatGPT for brainstorming, Notion for tracking tasks, Canva for branding, and PowerPoint for pitch decks. 

**EventForge** consolidates this entire 10-hour workflow into a 30-second AI generation process. You describe your event, and the AI handles the architecture: writing the copy, generating the logic trees, organizing tasks by department, and packaging it into ready-to-use shareable assets.

## 🚀 Key Features

*   **Intelligent Logic Trees**: Generates a deep event blueprint (timeline, tasks, budget, and marketing strategy) using Gemini's advanced contextual logic.
*   **Notion Workspace Automation**: Bypasses typical chat interfaces and actually creates a live, shared workspace with structured data across multiple Notion databases.
*   **PPTX Pitch Deck Synthesis**: Automatically exports key event info into a clean, Widescreen (16:9) presentation deck containing structured slides and visual guidance.
*   **Visual Persona & Brand ID**: Generates 3 unique "Poster Vibes" using custom-curated earth-tone palettes. Includes a full brand strategy and an AI Agent Brief for further creative scaling.
*   **Premium Glassmorphism UX**: A high-end, responsive dashboard built with modern CSS, focusing on dynamic user experience and premium aesthetics.

## 🛠️ Setup Instructions (For Judges/Local Dev)

1.  **Clone & Install**:
    ```bash
    git clone https://github.com/divyashah9999/EventForge.git
    cd EventForge
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```bash
    GEMINI_API_KEY=your_google_ai_key
    NOTION_TOKEN=your_notion_internal_integration_token
    NOTION_MASTER_PAGE_ID=your_shared_page_id
    ```
    *Note: Ensure your Notion Integration bot is invited to the Master Page!*

3.  **Run the Engine**:
    ```bash
    uvicorn server:app --host 0.0.0.0 --port 8000
    ```

4.  **Access the Dashboard**:
    Open `http://localhost:8000/ui/plan_a_new_event/code.html` in your browser.

## 🏗️ Technical Architecture

*   **Backend**: Python / FastAPI (Handles API abstractions and rate-limit buffering).
*   **AI Engine**: Google Gemini 2.5 Flash (Utilizing Strict JSON Output Schema for 100% predictable parsing).
*   **Platform Integrations**: Notion Client API (for complex database mutation), Python-PPTX.
*   **Frontend**: Vanilla HTML/JS with Material Design Tokens and Modern Glassmorphism CSS.

---
Built with ❤️ for the 2026 AI Innovation Hackathon.
