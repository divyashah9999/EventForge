import os
import time
import requests
from difflib import get_close_matches
from notion_client import Client
from notion_client.errors import APIResponseError
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

# Valid select options — must match what is patched into the Notion schema.
_DEPARTMENTS = ["PR & Media", "Logistics", "Tech", "Design"]
_STATUSES    = ["Not Started", "In Progress", "Done"]

def _normalize(value: str, options: list[str], fallback: str) -> str:
    """Fuzzy-match `value` to the closest entry in `options`.
    Uses case-insensitive matching with a 0.5 similarity cutoff.
    Falls back to `fallback` if nothing is close enough.
    """
    if not value:
        return fallback
    # Exact match (case-insensitive) first
    lower_map = {opt.lower(): opt for opt in options}
    if value.strip().lower() in lower_map:
        return lower_map[value.strip().lower()]
    # Fuzzy match
    matches = get_close_matches(value.strip().lower(), lower_map.keys(), n=1, cutoff=0.5)
    if matches:
        result = lower_map[matches[0]]
        print(f"  ⚡ Normalized '{value}' → '{result}'")
        return result
    print(f"  ⚠️  Could not normalize '{value}' — defaulting to '{fallback}'")
    return fallback

def _parse_markdown_table(md_string: str) -> dict:
    """Parses a simple markdown table string into a Notion table block."""
    lines = [line.strip() for line in (md_string or "").strip().split('\n') if line.strip()]
    if not lines:
        return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": md_string or ""}}]}}
    
    rows = []
    has_header = False
    for i, line in enumerate(lines):
        if line.startswith('|') and line.endswith('|'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            # Detect Markdown separator row like |---|---|
            if i == 1 and all(c.strip('-: ') == '' for c in cells):
                has_header = True
                continue
            rows.append(cells)
            
    if not rows:
        return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": md_string}}]}}
        
    table_width = len(rows[0])
    children = []
    for row in rows:
        while len(row) < table_width:
            row.append("")
        row = row[:table_width]
        
        cells_blocks = []
        for cell in row:
            # Notion table cells are arrays of rich text objects
            cells_blocks.append([{"type": "text", "text": {"content": cell}}])
            
        children.append({
            "type": "table_row",
            "table_row": {"cells": cells_blocks}
        })
        
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": has_header,
            "has_row_header": False,
            "children": children
        }
    }

def create_event_workspace(json_data: dict) -> str:
    root_page_id = os.getenv("NOTION_MASTER_PAGE_ID")
    print("🚀 Starting EventForge Workspace Generation...")

    # --- Step 1: Create Master Page ---
    master_page = notion.pages.create(
        parent={"type": "page_id", "page_id": root_page_id},
        properties={
            "title": {"title": [{"text": {"content": json_data["title"]}}]}
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": json_data["brief"]}}]
                }
            }
        ]
    )
    master_page_id = master_page["id"]
    print(f"✅ Master Page created: {master_page_id}")

    # --- Step 2: Create "PR & Media" sub-page ---
    pr_plan = json_data.get("pr_plan", {})
    pr_children = []
    
    # Social Calendar
    pr_children.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Social Calendar"}}]}})
    for msg in pr_plan.get("social_calendar", []):
        pr_children.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": msg}}]}})
        
    # Influencer Outreach
    pr_children.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Influencer Outreach"}}]}})
    for msg in pr_plan.get("influencer_outreach", []):
        pr_children.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": msg}}]}})
        
    # Email Template
    pr_children.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Email Template"}}]}})
    pr_children.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": pr_plan.get("email_template", "")}}]}})

    pr_page = notion.pages.create(
        parent={"page_id": master_page_id},
        properties={"title": {"title": [{"text": {"content": "PR & Media"}}]}},
        children=pr_children
    )
    print(f"✅ PR & Media sub-page created: {pr_page['id']}")

    # --- Step 3: Create "Logistics" sub-page ---
    log_plan = json_data.get("logistics_plan", {})
    logistics_children = []
    
    # Budget Table
    logistics_children.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Budget Table"}}]}})
    logistics_children.append(_parse_markdown_table(log_plan.get("budget_table", "")))
    
    # Hardware Checklist
    logistics_children.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Hardware Checklist"}}]}})
    for item in log_plan.get("hardware_checklist", []):
        logistics_children.append({"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": item}}], "checked": False}})
        
    # Venue Setup
    logistics_children.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Venue Setup"}}]}})
    logistics_children.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": log_plan.get("venue_setup", "")}}]}})

    logistics_page = notion.pages.create(
        parent={"page_id": master_page_id},
        properties={"title": {"title": [{"text": {"content": "Logistics"}}]}},
        children=logistics_children
    )
    print(f"✅ Logistics sub-page created: {logistics_page['id']}")

    # --- Step 4: Create Task Database ---
    db = notion.databases.create(
        parent={"type": "page_id", "page_id": master_page_id},
        title=[{"type": "text", "text": {"content": "Event Tasks"}}],
        is_inline=True,
        properties={
            "Name": {"title": {}},
            "Department": {"select": {"options": [
                {"name": "PR & Media"},
                {"name": "Logistics"},
                {"name": "Tech"},
                {"name": "Design"},
            ]}},
            "Status": {"select": {"options": [
                {"name": "Not Started"},
                {"name": "In Progress"},
                {"name": "Done"},
            ]}},
        }
    )
    database_id = db["id"]
    print(f"✅ Task database created: {database_id}")

    # WORKAROUND: notion-client SDK's databases.update() silently drops
    # the `properties` field from its PATCH body. Use raw HTTP instead.
    _token = os.getenv("NOTION_TOKEN")
    _patch_resp = requests.patch(
        f"https://api.notion.com/v1/databases/{database_id}",
        headers={
            "Authorization": f"Bearer {_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        json={
            "properties": {
                "Department": {"select": {"options": [
                    {"name": "PR & Media"},
                    {"name": "Logistics"},
                    {"name": "Tech"},
                    {"name": "Design"},
                ]}},
                "Status": {"select": {"options": [
                    {"name": "Not Started"},
                    {"name": "In Progress"},
                    {"name": "Done"},
                ]}},
            }
        }
    )
    saved_props = list(_patch_resp.json().get("properties", {}).keys())
    print(f"✅ Schema patched via raw PATCH — properties saved: {saved_props}")

    print("⏳ Waiting 5 seconds to ensure Notion API syncs the schema globally...")
    time.sleep(5)

    # --- Step 5: Populate database (with retry on validation_error) ---
    for task in json_data["tasks"]:
        dept   = _normalize(task.get("department", ""), _DEPARTMENTS, _DEPARTMENTS[0])
        status = _normalize(task.get("status", ""),     _STATUSES,    _STATUSES[0])
        task_props = {
            "Name": {"title": [{"text": {"content": task["name"]}}]},
            "Department": {"select": {"name": dept}},
            "Status": {"select": {"name": status}},
        }
        try:
            notion.pages.create(
                parent={"database_id": database_id},
                properties=task_props,
            )
            print(f"  ➕ Task added: {task['name']}")
        except APIResponseError as e:
            if "is not a property that exists" in str(e):
                print(f"  ⚠️  Schema not ready for '{task['name']}', forcing metadata refresh...")
                notion.databases.retrieve(database_id)  # force schema sync
                time.sleep(2)
                try:
                    notion.pages.create(
                        parent={"database_id": database_id},
                        properties=task_props,
                    )
                    print(f"  ➕ Task added (retry): {task['name']}")
                except APIResponseError as retry_err:
                    print(f"  ❌ Retry failed for '{task['name']}': {retry_err}")
            else:
                print(f"  ❌ Failed to add task '{task['name']}': {e}")

    # --- Step 6: Return the URL ---
    workspace_url = f"https://notion.so/{master_page_id.replace('-', '')}"
    print(f"\n🎉 Workspace ready: {workspace_url}")
    return workspace_url