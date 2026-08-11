# New Flows — Post-Production Extension System

> **Extending the AI Video Pre-Planning System into Post-Production Planning**
> Built on Elgendy Academy Workshops (Levels 8–11), enriched with professional execution methodology.

---

## How This Connects to the Existing System

```
┌─────────────────────────────────────────────────────┐
│   EXISTING: Video Pre-Planning Pipeline v3          │
│   (flowise_video_preplanning_flow)                  │
│                                                     │
│   Phase 0 → Phase 7                                 │
│   Intake → Brief → Strategy → Narrative →           │
│   Retention → Storyboard → Pacing → QA              │
│                                                     │
│   OUTPUT: Complete pre-planning package              │
│   (storyboard, pacing map, creative strategy, etc.)  │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼  feeds into
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────────┐   ┌───────────────────────┐
│ FLOW 1:           │   │ FLOW 2:               │
│ Post-Production   │   │ Speed Ramp &          │
│ Execution Flow    │   │ Viral Edit Flow       │
│                   │   │                       │
│ For: ALL projects │   │ For: Viral/short-form │
│ (ads, corporate,  │   │ speed ramp content    │
│  YouTube, docs,   │   │ ONLY                  │
│  brand films)     │   │                       │
│                   │   │ Alternative path —    │
│ 10 nodes          │   │ NOT sequential with   │
│ MANDATORY         │   │ Flow 1                │
│                   │   │                       │
│                   │   │ 7 nodes               │
│                   │   │ OPTIONAL              │
└───────────────────┘   └───────────────────────┘
```

## Which Flow to Use?

| Your Project Type | Use This Flow |
|------------------|---------------|
| Commercial / Ad | Flow 1 |
| YouTube long-form | Flow 1 |
| Corporate / Brand video | Flow 1 |
| Documentary | Flow 1 |
| Event highlight | Flow 1 |
| Product showcase | Flow 1 |
| Infographic / Animation video | Flow 1 |
| **Viral speed ramp edit** | **Flow 2** |
| **TikTok/Reels speed ramp content** | **Flow 2** |
| **Trendy short-form with speed manipulation** | **Flow 2** |

> **Rule**: Use Flow 1 for everything UNLESS your project specifically revolves around speed ramping and viral short-form editing. Flow 2 is a specialized alternative, not an add-on.

---

## Folder Structure

```
new flows/
├── README.md                              ← You are here
│
├── 01_post_production_execution_flow/     ← FLOW 1 (mandatory for all projects)
│   ├── README.md                          ← Setup guide
│   ├── system_overview.md                 ← Full system documentation
│   └── nodes/
│       ├── 01_start_intake.md
│       ├── 02_asset_organization.md
│       ├── 03_first_cuts_strategist.md
│       ├── 04_effects_transition_designer.md
│       ├── 05_motion_graphics_planner.md
│       ├── 06_sound_design_architect.md
│       ├── 07_audio_mixing_mastering.md
│       ├── 08_color_finishing.md
│       ├── 09_self_critique.md
│       └── 10_execution_package.md
│
└── 02_speed_ramp_viral_flow/              ← FLOW 2 (optional, viral content only)
    ├── README.md
    ├── system_overview.md
    └── nodes/
        ├── 01_start_intake.md
        ├── 02_clip_arrangement.md
        ├── 03_speed_ramp_designer.md
        ├── 04_viral_effects.md
        ├── 05_sound_finishing.md
        ├── 06_self_critique.md
        └── 07_viral_package.md
```

---

## Source Material

These flows are built from the following Elgendy Academy workshops:

| Workshop | What It Taught | Where It's Used |
|----------|---------------|-----------------|
| **Level 8**: F1 Ad Workshop (Premiere + AE) | Full ad production: script → first cuts → effects → 4-layer sound design → mixing → logo animation | Flow 1 (all nodes) |
| **Level 9**: Infographics Workshop (Premiere + AE) | Brief analysis, visual feeding, 3D text/tracking, motion graphics, callouts, masks | Flow 1 (nodes 02, 05) |
| **Level 10**: Trendy Transitions & Effects (AE) | Effects catalog, 3D camera transitions, mask transitions, rotoscoping, cyber effects | Flow 1 (nodes 04, 05) |
| **Level 11**: Viral Speed Ramp Workshop (AE) | Speed ramping, graph editor, particles, turbulent displace, finishing | Flow 2 (all nodes) |

---

## Prerequisites

- A completed **Video Pre-Planning Package** from the existing preplanning flow
- Flowise v2.0+ (with AgentFlow V2 support)
- An LLM API key (Claude / Gemini / GPT-4o recommended)
- Recommended: High-capability model for Effects Designer and Sound Design nodes (100K+ context)
