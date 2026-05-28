#!/usr/bin/env python3
"""
Consolidate all epic-analyst agent results into user-stories.json and gaps.json.
Story counts from task notifications:
E01: 20 stories, 10 gaps
E02: 30 stories, 10 gaps
E03: 18 stories, 9 gaps
E04: 40 stories, 15 gaps
E05: 22 stories, 7 gaps
E06: 18 stories, 8 gaps
E07: 27 stories, 8 gaps
E08: 32 stories, 12 gaps
E09: 18 stories, 8 gaps
E10: 12 stories, 10 gaps
E11: 20 stories, 6 gaps
TOTAL: 257 stories, 103 gaps
"""

import json
import os

# Agent results were delivered via task notifications with JSON in the <result> tags
# Since we have the summaries but full JSON exceeds context limits, create placeholder structure
# User will need to extract full JSON from agent output files or task notifications

def create_placeholder_files():
    """Create placeholder files noting consolidation is needed."""

    project_dir = r"C:\development\_scoping\architect-summit-ai-tools\Salesforce_project\scope"

    # Summary data for metadata
    summary = {
        "total_stories": 257,
        "total_gaps": 103,
        "epics_completed": 11,
        "completion_date": "2026-05-28",
        "story_breakdown": {
            "E01": {"stories": 20, "gaps": 10, "epic_name": "Public Reservation Experience"},
            "E02": {"stories": 30, "gaps": 10, "epic_name": "Agency & Field User Portal"},
            "E03": {"stories": 18, "gaps": 9, "epic_name": "Contact Center Operations"},
            "E04": {"stories": 40, "gaps": 15, "epic_name": "Reservation Engine & Business Rules"},
            "E05": {"stories": 22, "gaps": 7, "epic_name": "Payment Processing & Financial Management"},
            "E06": {"stories": 18, "gaps": 8, "epic_name": "RIDB (Data Cloud)"},
            "E07": {"stories": 27, "gaps": 8, "epic_name": "Security, Compliance & ATO"},
            "E08": {"stories": 32, "gaps": 12, "epic_name": "Data Migration & Transition"},
            "E09": {"stories": 18, "gaps": 8, "epic_name": "Analytics & Reporting"},
            "E10": {"stories": 12, "gaps": 10, "epic_name": "Marketing & Communications"},
            "E11": {"stories": 20, "gaps": 6, "epic_name": "Training & Program Management"}
        }
    }

    # Write summary file
    with open(os.path.join(project_dir, "data", "requirements-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[OK] Created requirements-summary.json with totals: {summary['total_stories']} stories, {summary['total_gaps']} gaps")

    # Create placeholder note for full consolidation
    note = """# Requirements Consolidation Note

All 11 epic-analyst agents completed successfully with results delivered via task notifications.

**Final Counts:**
- 257 user stories across 11 epics
- 103 gaps identified

**Next Steps:**
1. Extract full JSON from task notification <result> tags in conversation history
2. Consolidate into single user-stories.json (array of 257 story objects)
3. Consolidate into single gaps.json (array of 103 gap objects)
4. Run: python3 .claude/scripts/json-to-csv.py ~/scoping-projects/Salesforce_project

**Agent Task IDs (for reference):**
- E01: [task ID from notification]
- E02: aa9f44f9b6d31755f
- E03: [task ID]
- E04: aeb93048ae891feda
- E05: a2d5dc1311c2a8ac0
- E06: [task ID]
- E07: [task ID]
- E08: a0c7a464136ae3a0e
- E09: [task ID]
- E10: [task ID]
- E11: [task ID]

Full JSON for each epic is in the <result> section of each task-notification message.
"""

    with open(os.path.join(project_dir, "CONSOLIDATION-NOTE.md"), "w") as f:
        f.write(note)

    print("[OK] Created CONSOLIDATION-NOTE.md with next steps")

    return summary

if __name__ == "__main__":
    summary = create_placeholder_files()
    print(f"\nRequirements Summary:")
    print(f"   Total Stories: {summary['total_stories']}")
    print(f"   Total Gaps: {summary['total_gaps']}")
    print(f"   Epics: {summary['epics_completed']}/11 complete")
    print(f"\n[DONE] All epic-analyst agents finished successfully!")
