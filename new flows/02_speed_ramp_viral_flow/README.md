# Flow 2: Speed Ramp & Viral Edit Flow — Setup Guide

> A specialized post-production flow for viral, high-energy short-form content built around speed ramping — derived from Elgendy Academy Workshop Level 11 (Viral Speed Ramp) and Level 10 (Trendy Transitions).

> **🔌 Import directly into Flowise**: [Speed_Ramp_Viral_Flow_v1.json](./Speed_Ramp_Viral_Flow_v1.json) — 11 nodes, all prompts pre-wired.

---

## Overview

This flow is an **alternative to Flow 1** — not an add-on. Use it when your project is specifically a viral, speed-ramp-driven short-form edit (TikTok, Reels, YouTube Shorts, montage reels, showreels).

The entire flow is optimized for After Effects-first editing, speed manipulation, trendy effects, and maximum visual impact in short duration.

---

## Architecture

```
START (receives preplanning output + clips info)
  → Clip Arrangement & Selection
  → Speed Ramp Designer
  → Viral Effects & Transitions
  → Sound Design & Finishing
  → Self-Critique
  → [Condition: Grade ≥ A?]
      → YES → Final Viral Package → END
      → NO  → Loop back to Speed Ramp Designer (max 2 revisions)
```

### Node Summary

| # | Node Type | File | Purpose |
|---|-----------|------|---------|
| 1 | Start Node (Form) | `01_start_intake.md` | Receives preplanning package + viral-specific inputs |
| 2 | LLM Node | `02_clip_arrangement.md` | Clip selection, ordering, and arrangement strategy |
| 3 | LLM Node | `03_speed_ramp_designer.md` | Speed ramp curves, timing, and graph editor planning |
| 4 | LLM Node | `04_viral_effects.md` | Trendy effects, transitions, masks, particles |
| 5 | LLM Node | `05_sound_finishing.md` | Sound design + color + finishing (combined for efficiency) |
| 6 | LLM Node | `06_self_critique.md` | Audits against viral content standards |
| 7 | LLM Node | `07_viral_package.md` | Final compiled package |

---

## Flow State Variables

```json
{
  "preplanning_package": "",
  "project_brief": "",
  "storyboard": "",
  "pacing_map": "",
  "creative_strategy": "",
  "clip_arrangement": "",
  "speed_ramp_plan": "",
  "viral_effects_plan": "",
  "sound_finishing_plan": "",
  "critique_report": "",
  "critique_grade": "",
  "revision_count": 0,
  "viral_package": ""
}
```

---

## When to Use This Flow

✅ **Use this flow when:**
- The project is a speed ramp / montage / showreel
- Content is short-form (15-60 seconds)
- The goal is viral, high-energy impact
- Speed manipulation is a core technique
- The footage is action-oriented (sports, cars, dance, parkour, travel)

❌ **Do NOT use this flow when:**
- The project has dialogue, VO, or narrative
- The project needs infographics, callouts, or data visualization
- The project is corporate, documentary, or interview-based
- Speed ramping is just one element, not the core technique

---

## Setup in Flowise

Same process as Flow 1:
1. Create new AgentFlow: `Speed Ramp Viral Pipeline`
2. Add Start Node with form fields from `01_start_intake.md`
3. Add LLM Nodes (02-07) with system prompts from each file
4. Add Condition Node after Self-Critique (node 06)
5. Connect and test
