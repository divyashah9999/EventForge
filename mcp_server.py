# mcp_server.py
import sys
import os

# Crucial: Ensure the server runs from its own directory so .env is found
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

# Force UTF-8 for Windows terminals to avoid encoding errors in MCP transport
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mcp.server.fastmcp import FastMCP
from main import run_eventforge

# Initialize FastMCP - This name will appear in Stitch/Antigravity
mcp = FastMCP("EventForge")

@mcp.tool()
def forge_event(prompt: str) -> dict:
    """
    Acts as a high-level Event COO. Generates a full Notion workspace 
    and a PPTX Pitch Deck from a natural language event idea.
    
    Args:
        prompt: The event idea or description (e.g., 'A blockchain hackathon').
    """
    print(f"🚀 MCP Tool called with prompt: {prompt}", file=sys.stderr)
    return run_eventforge(prompt)

if __name__ == "__main__":
    mcp.run()