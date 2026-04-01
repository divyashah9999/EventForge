"""
EventForge Orchestrator — Phase 5
Pipeline: User Prompt → Gemini JSON → Notion Workspace + PPTX Pitch Deck
"""
import sys
from dotenv import load_dotenv

load_dotenv()


def run_eventforge(user_prompt: str) -> dict:
    """
    Full three-stage pipeline. Notion and PPTX run independently —
    a failure in one does not cancel the other.
    """
    results = {
        "status":          "partial",
        "workspace_url":   None,
        "pitch_deck_path": None,
        "errors":          [],
    }

    # ── Stage 1: Gemini planning ──────────────────────────────────────────────
    from gemini_agent import generate_event_data
    event_json = generate_event_data(user_prompt)   # raises on hard failure
    print("\n✅ Gemini Planning Complete")

    # ── Stage 2: Notion workspace ─────────────────────────────────────────────
    try:
        from notion_agent import create_event_workspace
        results["workspace_url"] = create_event_workspace(event_json)
        print(f"✅ Notion Workspace: {results['workspace_url']}")
    except Exception as e:
        results["errors"].append(f"Notion failed: {e}")
        print(f"❌ Notion failed: {e}")

    # ── Stage 3: PPTX pitch deck ──────────────────────────────────────────────
    try:
        from pptx_agent import generate_pitch_deck
        results["pitch_deck_path"] = generate_pitch_deck(event_json)
        print(f"✅ Pitch Deck Saved: {results['pitch_deck_path']}")
    except Exception as e:
        results["errors"].append(f"PPTX failed: {e}")
        print(f"❌ PPTX failed: {e}")

    if not results["errors"]:
        results["status"] = "success"

    return results


def main():
    print("============================================================")
    print("                  EventForge CLI ⚡")
    print("============================================================")

    # Accept prompt from CLI arg or interactive input
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(f"Event Idea (from args): {prompt}")
    else:
        print("Describe your event. The AI will generate a Notion workspace")
        print("AND a PowerPoint pitch deck — automatically.\n")
        try:
            prompt = input("Event Idea: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)

    if not prompt.strip():
        print("❌ No input provided. Exiting.")
        sys.exit(1)

    print("\n" + "=" * 60)

    try:
        results = run_eventforge(prompt)
    except Exception as e:
        # Only reaches here if Gemini itself fails (hard failure)
        print(f"\n❌ Gemini planning failed: {e}")
        sys.exit(1)

    # ── Final Summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("EVENTFORGE COMPLETE")
    print("=" * 60)
    if results["workspace_url"]:
        print(f"  Notion Workspace : {results['workspace_url']}")
    if results["pitch_deck_path"]:
        print(f"  Pitch Deck       : {results['pitch_deck_path']}")
    if results["errors"]:
        print(f"\n  Warnings:")
        for err in results["errors"]:
            print(f"    - {err}")
    print("=" * 60)


if __name__ == "__main__":
    main()
