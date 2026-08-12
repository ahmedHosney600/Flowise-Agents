# Flow 1: Post-Production Execution Flow — Setup Guide

> The complete post-production planning pipeline. Takes your pre-planning package and produces a detailed, step-by-step execution blueprint for the editor.

---

## Overview

This flow picks up where the Video Pre-Planning Pipeline ends. Instead of a storyboard that says *what* each shot should contain, this flow produces a detailed plan for *how* to build it — covering asset organization, cutting strategy, specific effects and transitions, motion graphics, 4-layer sound design, audio mixing, and color finishing.

> **🔌 Import directly into Flowise**: [Post_Production_Execution_Flow_v1.json](./Post_Production_Execution_Flow_v1.json) — 15 nodes, all prompts pre-wired.

---

## Architecture

```
START (receives preplanning output)
  → Asset Organization & Visual Feeding
  → [GATE: Human Input] ─ confirm assets & direction match reality
  → First Cuts Strategist
  → Effects & Transition Designer
  → Motion Graphics & Compositing Planner
  → Sound Design Architect (4-Layer)
  → Audio Mixing & Mastering
  → Color Grading & Finishing
  → Self-Critique (Audit Only)
  → [Condition: Grade contains "A"?]
       → YES → Final Execution Package → END
       → NO  → Revision Applier (09a) → loop back to Effects Designer (max 2)
```

### Node Summary

| # | Node Type | File | Purpose |
|---|-----------|------|---------|
| 1 | Start Node (Form) | `01_start_intake.md` | Receives preplanning package + project-specific inputs |
| 2 | LLM Node | `02_asset_organization.md` | Plans file structure, footage sourcing, visual references |
| 2a | Human Input Node | *(built-in)* | Gate: user confirms assets match reality before downstream work |
| 3 | LLM Node | `03_first_cuts_strategist.md` | First cuts methodology — shot selection, ordering, timing |
| 4 | LLM Node | `04_effects_transition_designer.md` | Per-shot effects, transitions, overlays, compositing techniques |
| 5 | LLM Node | `05_motion_graphics_planner.md` | 3D text, tracking, callouts, infographic elements, logo animation |
| 6 | LLM Node | `06_sound_design_architect.md` | 4-layer sound blueprint: ambiance → essentials → SFX → hits |
| 7 | LLM Node | `07_audio_mixing_mastering.md` | Levels, EQ, reverb, panning, sub-mixes, gain staging |
| 8 | LLM Node | `08_color_finishing.md` | Color grading, overlays, grain, vignette, final polish |
| 9 | LLM Node | `09_self_critique.md` | Audit only — grade, list of issues, per-issue fix instructions |
| 9a | LLM Node | `09a_revision_integrator.md` | Applies CRITICAL/WARNING fixes → drops in revised plan sections |
| 10 | LLM Node | `10_execution_package.md` | Final compiled editor handoff package |

**Why two critique nodes?** Node 09 is a pure auditor — it reads everything but writes nothing except a report + grade. Revision Applier (09a) runs lazily: only when the audit fails. On Grade-A runs (typical majority), this skips the whole revision pass and saves a full LLM round-trip across every plan section.

---

## Flow State Variables

```json
{
  "preplanning_package": "",
  "project_brief": "",
  "storyboard": "",
  "pacing_map": "",
  "creative_strategy": "",
  "asset_plan": "",
  "asset_human_approved": false,
  "asset_human_notes": "",
  "first_cuts_plan": "",
  "effects_plan": "",
  "motion_graphics_plan": "",
  "sound_design_plan": "",
  "mixing_plan": "",
  "color_plan": "",
  "critique_report": "",
  "critique_grade": "",
  "revised_plans": "",
  "revision_count": 0,
  "execution_package": ""
}
```

---

## Step-by-Step Setup in Flowise

### Step 1: Create a New AgentFlow
1. In Flowise, click **AgentFlows** → **Add New**
2. Name it: `Post-Production Execution Pipeline`

### Step 2: Add the Start Node
1. Drag a **Start Node** onto the canvas
2. Set Input Type to **formInput** (or **chatInput** if you prefer pasting)
3. Add form fields from `01_start_intake.md`
4. Configure Flow State with the JSON above

### Step 3: Add LLM Nodes (one per phase)
1. For each file in `nodes/` (02 through 10):
   - Drag an **LLM Node** onto the canvas
   - Connect your Chat Model (Claude Sonnet 4 / Gemini 2.5 Pro recommended)
   - Copy the **System Prompt** from the file
   - Set the output variable per the file's instructions
2. **Exception — 09a**: Only add this node's prompt; connect it lazily via the condition. It runs only on sub-A grades.

### Step 3b: Add Human Input Gate (after Asset Organization)
1. After Node 02 (Asset Organization), add a **Human Input** node.
2. Set input type to **formInput** with these fields:
   - `assetApproved` (dropdown): `Continue to first cuts` / `Pause — adjust assets first`
   - `adjustmentNotes` (multiline): "Which assets/sourcing/music choices need to change?"
3. The node pauses the flow and surfaces Node 02's asset summary + sourcing plan
4. When the user selects **Continue**, store their notes in `{{ $flow.state.asset_human_notes }}` and proceed to Node 03
5. When **Pause**, the user can edit the brief/assets and re-run Node 02 (loop wired back)

### Step 4: Add Condition Node (Self-Critique Gate)
1. After node 09 (Self-Critique), add a **Condition Node**
2. Set condition: `{{$flow.state.critique_grade}}` contains "A"
   - **True** → Final Execution Package
   - **False** → Run Revision Applier (node 09a)
3. Failsafe: if `{{$flow.state.revision_count}}` >= 2, force continue

### Step 5: Connect & Test
Follow the architecture diagram. Test with a completed preplanning package.

---

## Tips

- **Input**: This flow expects the output from the Video Pre-Planning Pipeline. You can paste the final package directly, or connect the two flows.
- **Token management**: The Effects Designer (node 04) and Sound Design (node 06) are the most token-intensive. Use 100K+ context models.
- **Model selection**: You can use different models per node. Cheaper models work fine for Asset Organization and Color Finishing. Use premium models for Effects and Sound Design.
- **Modularity**: If you only need sound design planning, you can run just nodes 01 → 06 → 07 independently.
