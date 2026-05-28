# exmaple_project — Scopezilla Project

**Depth mode**: story-level (full user stories per epic, story-level estimates)  
**RFP tier**: express (light-weight RFI response)  
**Vertical**: (none)

This is a Scopezilla scoping project. When working in this folder:

- Read `data/memory.json` at the start of each session for context
- Update `data/memory.json` at the end of each session with outcomes and open threads
- Use the Scopezilla skills (discover, requirements, design, etc.) to build deliverables
- All outputs go to `outputs/` — never overwrite existing files without asking

## Project Structure

- `discovery-notes/` — Drop your RFPs, transcripts, meeting notes here
- `knowledge/` — Reference docs (Salesforce implementation guides, best practices)
- `reference/` — Additional context materials
- `data/` — Structured scoping data (epics, gaps, stories, memory)
- `outputs/` — Generated deliverables (Word docs, Excel, slide decks)

## Workflow

1. **discover** — Ingest discovery documents, produce project summary
2. **strategy** — Develop business case, value proposition, transformation narrative
3. **requirements** — Define epics, write user stories, identify gaps
4. **design** — Technical architecture, solution brief, T-shirt sizing
5. **validate** — Quality gate before handoff
6. **export** — Package deliverables for the client

Run `/skill scopezilla-dev:next` if you're unsure what to do.

## Support

Stuck or have feedback? Post in [#help-scopezilla](https://salesforce.enterprise.slack.com/archives/C09T23WKM8Q) or run `/skill scopezilla-dev:help`.
