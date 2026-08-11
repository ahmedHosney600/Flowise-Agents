# Flowise Video Pre-Planning System — Setup Guide

> This is the **Flowise AgentFlow V2** version of the Video Pre-Planning System.
> For the manual copy-paste version (for use in Claude/Gemini web interfaces), see `../video_preplanning_system.md`.

---

## Overview

This folder contains everything you need to build an automated video pre-planning pipeline in Flowise. Instead of manually copying prompts between phases, the AgentFlow runs the entire 8-phase pipeline automatically — you just fill in a form and get a complete, editor-ready pre-planning package.

---

## Prerequisites

- Flowise v2.0+ (with AgentFlow V2 support)
- An LLM API key (Anthropic Claude, Google Gemini, or OpenAI)
- Recommended model: Claude Sonnet 4 / Gemini 2.5 Pro / GPT-4o (high capability needed for storyboard generation)

---

## Architecture

```
START (Form) → Brief Builder → Human Approval → Creative Strategy
    → Narrative Structure → Retention Engineering → Storyboard Builder
    → Pacing & Rhythm → Self-Critique → [Condition: Grade ≥ A?]
        → YES → QA & Final Package → END
        → NO  → Loop back to Storyboard (max 2 revisions)
```

### Node Summary

| # | Node Type | File | Purpose |
|---|-----------|------|---------|
| 1 | Start Node (Form) | `01_start_intake.md` | Collects all project info via structured form fields |
| 2 | LLM Node | `02_brief_builder.md` | Compiles form answers into a formatted Project Brief |
| 3 | Human Input Node | *(built-in Flowise node)* | User reviews and approves the brief |
| 4 | LLM Node | `03_creative_strategy.md` | Determines editing style, music, references, visual mood |
| 5 | LLM Node | `04_narrative_structure.md` | Designs the storytelling arc with hooks and open loops |
| 6 | LLM Node | `05_retention_engineer.md` | Engineers pattern interrupts, drop-off fixes, micro-hooks |
| 7 | LLM Node | `06_storyboard_builder.md` | Generates shot-by-shot storyboard with sound design |
| 8 | LLM Node | `07_pacing_rhythm.md` | Creates beat map, energy curve, silence placement |
| 9 | LLM Node | `08_self_critique.md` | Audits storyboard against all methodology rules |
| 10 | Condition Node | *(built-in)* | Routes based on critique grade (A+ → continue, else → loop) |
| 11 | LLM Node | `09_qa_final_package.md` | Final QA checklist + compiled deliverable package |
| 12 | End Node | *(built-in)* | Returns the final output |

---

## Flow State Variables

Initialize these in the Start Node under **Flow State**:

```json
{
  "project_brief": "",
  "creative_strategy": "",
  "narrative_structure": "",
  "retention_map": "",
  "storyboard": "",
  "pacing_map": "",
  "critique_report": "",
  "critique_grade": "",
  "revision_count": 0,
  "final_package": ""
}
```

Each LLM Node reads from prior state variables and writes its output to its designated variable.

---

## Step-by-Step Setup in Flowise

### Step 1: Create a New AgentFlow
1. In Flowise, click **AgentFlows** → **Add New**
2. Name it: `Video Pre-Planning Pipeline`

### Step 2: Add the Start Node
1. Drag a **Start Node** onto the canvas
2. Set Input Type to **formInput**
3. Add all form fields listed in `01_start_intake.md`
4. Configure the Flow State with the JSON above

### Step 3: Add LLM Nodes (one per phase)
1. For each file in the `nodes/` folder (02 through 09):
   - Drag an **LLM Node** onto the canvas
   - Connect your Chat Model (Claude/Gemini/GPT)
   - Copy the **System Prompt** from the file into the node's system message
   - Set the **output variable** to write to the corresponding Flow State key

### Step 4: Add Human Input Node
1. After the Brief Builder (Node 2), add a **Human Input Node**
2. This pauses the flow so you can review the generated brief
3. You can approve or provide corrections

### Step 5: Add Condition Node (Self-Critique Gate)
1. After the Self-Critique node (Node 9), add a **Condition Node**
2. Set condition: Check if `{{$flow.state.critique_grade}}` contains "A"
   - **True path** → connects to QA & Final Package node
   - **False path** → connects back to Storyboard Builder node (Loop)
3. Add a secondary condition: if `{{$flow.state.revision_count}}` >= 2, force continue to QA (prevents infinite loops)

### Step 6: Add End Node
1. After the QA & Final Package node, add an **End Node**
2. Set it to return `{{$flow.state.final_package}}`

### Step 7: Connect All Nodes
Follow the architecture diagram above to connect nodes with edges.

### Step 8: Test
1. Click **Run** or **Chat**
2. Fill in the intake form
3. Watch the pipeline process through all phases
4. Review the final output

---

## Tips

- **Optional Fields**: Only 7 fields are required (video topic, primary goal, core message, content type, target duration, target audience, and primary platform). All other fields are optional — the Brief Builder will automatically apply smart, context-aware defaults for any unanswered fields. No more "System Flag" errors from missing data.
- **Token Management**: The Storyboard Builder (Phase 4) is the most token-intensive node. Use a model with at least 100K context window.
- **Timeout Settings**: Increase Flowise timeout settings if your LLM takes long on the storyboard generation.
- **Testing Individual Nodes**: You can temporarily disconnect downstream nodes to test each phase independently.
- **Model Selection**: You can use different models per node. For example, use a cheaper model for Brief Builder and a premium model for Storyboard Builder.

---

## File Reference

| File | What It Contains |
|------|-----------------|
| `01_start_intake.md` | All 25 form field definitions with types and options |
| `02_brief_builder.md` | System prompt: compiles form → structured brief |
| `03_creative_strategy.md` | System prompt: brief → creative strategy + style analysis |
| `04_narrative_structure.md` | System prompt: brief + strategy → narrative arc |
| `05_retention_engineer.md` | System prompt: narrative → retention-engineered structure |
| `06_storyboard_builder.md` | System prompt: all above → shot-by-shot storyboard (includes shot type & transition references) |
| `07_pacing_rhythm.md` | System prompt: storyboard → pacing map (includes platform DNA & sound design references) |
| `08_self_critique.md` | System prompt: storyboard + pacing → critique & revision (includes common mistakes reference) |
| `09_qa_final_package.md` | System prompt: everything → final QA + compiled package |
