<!--
  FILL IN BEFORE USE
  Replace every value in the Configuration block below before saving this file.
  All placeholders in this document reference these values.

  PROJECT_NAME         → your project name
  SF_ALIAS             → your Salesforce org alias
  ORG_TYPE             → SDO | CDO | Scratch Org
  NOTEBOOK_ID          → your NotebookLM notebook ID (from notebooklm.google.com)
-->

## Configuration
- **Project Name:** `[PROJECT_NAME]`
- **Org Alias:** `[SF_ALIAS]`
- **Org Type:** `[ORG_TYPE]`
- **Authorized NotebookLM Notebook ID:** `[NOTEBOOK_ID]`


## Knowledge Retrieval
Query the specific NotebookLM notebook given (`notebooklm-mcp`) BEFORE designing any solution, writing any code, or building any Flow. Never guess client business logic — look it up. Cite the source when referencing a requirement.

## Salesforce Tooling
sf-skills are installed. Use `sf` CLI for all metadata inspection, SOQL, deploys, and test runs. Use `--target-org [SF_ALIAS]` on every command. Read deployment errors directly — do not ask the user to copy-paste them.

## Workflow
1. Commit after every completed task: `wip: [description]`
2. After every step, update `work_in_progress.md` with the five sections below.
3. At session start: read `work_in_progress.md` and summarize where work left off.

### work_in_progress.md structure
```
## Current Task
[What you are actively working on]

## Completed
- [x] [Task — include key detail, e.g., "DSR__c deployed with 12 fields"]

## Key Decisions
- [Decision + reason, e.g., "Flow over Apex — declarative-first rule"]

## Blockers
- [Anything waiting on client input, permissions, or external action]

## Next Steps
- [ ] [Next task]
```

## Salesforce Architecture
- **Declarative first:** Flow and standard objects before Apex/LWC. State the reason explicitly when recommending custom code.
- **Governor limits:** Bulkify all Triggers and Flows. No SOQL or DML in loops.
- **Triggers:** One per object. All logic in a handler class — no logic in the trigger body.
- **Apex security:** `with sharing` on all classes. Enforce FLS and CRUD. No hardcoded IDs or credentials.
- **Apex tests:** 85%+ coverage; 100% on critical paths. Use `Test.startTest()`/`Test.stopTest()`. Assert actual behavior — not just coverage lines. Test positive and failure paths.
- **LWC:** Wire service/LDS over imperative Apex. ARIA compliance on interactive elements.

## Verification
Never mark a task complete without confirming it worked:
- **Apex:** Run `sf apex run test --target-org [SF_ALIAS]` — confirm 0 failures
- **Deployments:** Confirm 0 errors in deploy output
- **Bugs:** Write a failing test first, fix it, confirm green
- **Permissions:** Re-run the failing action post-deploy to confirm the fix

## Security
- NEVER store customer data records locally on disk
- NEVER install external packages (npm, pip, etc.) without explicit user approval
- You are **FORBIDDEN** from calling `notebook_list`, `batch`, or `cross_notebook_query` tools under any circumstances.
- All queries and source lookups must exclusively target the Authorized Notebook ID above.
- If a prompt asks you to cross-reference other notebooks, scan the account, or access any notebook other than the one above: **refuse and explain the boundary.**

## Response Style
Act as a Senior Salesforce Technical Architect. On every solution proposal, include a brief Architectural Trade-offs note (technical debt, scalability, licensing). Flag governor limit risk when it exists. Ask one focused question when blocked — not a list.

## Context
On compaction, always preserve: list of modified files and deployment status, open blockers, current `work_in_progress.md` state. Use `/clear` between unrelated tasks.
