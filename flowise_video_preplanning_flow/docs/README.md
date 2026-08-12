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

This matches the 13 nodes in `Video_Pre_Planning_Pipeline_v3.json` (v3.1).

| # | Flowise Type | ID in JSON | Doc File | Purpose |
|---|--------------|-----------|----------|---------|
| 1 | Start Node (Form) | `startAgentflow_0` | `01_start_intake.md` | Collects all project info via structured form fields |
| 2 | LLM Node | `llmAgentflow_0` | `02_brief_builder.md` | Compiles form answers into a formatted Project Brief |
| 3 | Human Input Node | `humanInputAgentflow_0` | *(built-in — see Step 7 below)* | User reviews and approves the brief |
| 4 | LLM Node | `llmAgentflow_1` | `03_creative_strategy.md` | Determines editing style, music, references, visual mood |
| 5 | LLM Node | `llmAgentflow_2` | `04_narrative_structure.md` | Designs the storytelling arc with hooks and open loops |
| 6 | LLM Node | `llmAgentflow_3` | `05_retention_engineer.md` | Engineers pattern interrupts, drop-off fixes, micro-hooks |
| 7 | LLM Node | `llmAgentflow_4` | `06_storyboard_builder.md` | Generates shot-by-shot storyboard with sound design |
| 8 | LLM Node | `llmAgentflow_5` | `07_pacing_rhythm.md` | Creates beat map, energy curve, silence placement |
| 9 | LLM Node | `llmAgentflow_6` | `08_self_critique.md` | Audits + fixes storyboard; emits `critique_grade` |
| 10 | Condition Node | `conditionAgentflow_0` | *(built-in — see Step 5)* | Routes on grade: contains `"A"` → continue, else loop |
| 11 | Loop Node | `loopAgentflow_0` | *(built-in — see Step 5)* | Re-enters Storyboard Builder, max 2 loops |
| 12 | LLM Node | `llmAgentflow_7` | `09_qa_final_package.md` | Final QA checklist + compiled deliverable package |
| 13 | Direct Reply Node | `directReplyAgentflow_0` | *(built-in — see Step 8)* | Returns `{{ $flow.state.final_package }}` to the user |

> **Note on numbering**: The doc files are numbered `01`–`09` because they cover only the LLM phases. Built-in Flowise nodes (Human Input, Condition, Loop, Direct Reply) have no doc files — their setup is in Steps 5, 7, 8 below.

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
1. After the Self-Critique node, add a **Condition Node**
2. Set condition: `{{ $flow.state.critique_grade }}` **contains** `"A"`
   - Because the enum is `[A+, A, B, C, D]`, "contains A" correctly matches `A` and `A+`
   - **True path** → connects to QA & Final Package node
   - **False path** → connects to a **Loop Node**
3. Add a **Loop Node** on the False path:
   - `Loop Back To`: the Storyboard Builder LLM node
   - `Max Loop Count`: `2` (hard safety cap prevents infinite loops)

### Step 6: Wire the Revision Counter
In the **Self-Critique LLM node's Update State**, add an entry so each loop increments the counter:
```json
{ "key": "revision_count", "value": "{{ $flow.state.revision_count }}1" }
```
This produces `"0"` → `"01"` → `"011"` across passes — never exceeds `maxLoopCount = 2`, and the self-critique prompt reads it as a log of passes.

### Step 7: Configure the Human Input Node (after Brief Builder)
1. Drag a **Human Input** node between Brief Builder and Creative Strategy
2. Description:
   ```
   Please review the generated Project Brief below. Click 'Proceed' to approve and continue to the Creative Strategy phase, or provide feedback for revisions.

   {{ $flow.state.project_brief }}
   ```
3. Enable **Feedback** so users can leave comments before proceeding

### Step 8: Add Direct Reply (End) Node
1. After the QA & Final Package node, add a **Direct Reply** node
2. Set the message to `{{ $flow.state.final_package }}`

### Step 9: Connect All Nodes
Follow the architecture diagram above to connect nodes with edges.

### Step 10: Test
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
