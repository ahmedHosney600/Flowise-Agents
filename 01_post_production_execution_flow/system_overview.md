# Post-Production Execution Flow — System Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    START NODE (Form Input)                    │
│  Receives: Pre-planning package + editor-specific inputs     │
│  Initializes: All flow state variables                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│            NODE 02: Asset Organization & Visual Feeding       │
│  • Parses preplanning package into sections                  │
│  • Designs project folder structure                          │
│  • Plans footage sourcing per shot                           │
│  • Creates visual feeding reference plan                     │
│  OUTPUT → asset_plan, project_brief, storyboard, pacing_map │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              NODE 03: First Cuts Strategist                   │
│  • Storyboard-to-timeline translation                        │
│  • Hook construction plan                                    │
│  • Cut point decisions (on action, on beat, match cut)       │
│  • VO/music sync mapping                                     │
│  • Timeline track structure                                  │
│  OUTPUT → first_cuts_plan                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│          NODE 04: Effects & Transition Designer    ◄──┐      │
│  • Per-cut transition design (flash, mask, 3D, match)  │      │
│  • Per-shot effect design (overlays, blur, glow)       │      │
│  • AE composition planning                             │      │
│  • Plugin requirements + alternatives                  │      │
│  OUTPUT → effects_plan                                 │      │
└─────────────────────┬──────────────────────────────────│────┘
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│          NODE 05: Motion Graphics Planner            │  │
│  • Text/title animations                             │  │
│  • 3D text & camera tracking                         │  │
│  • Callouts, annotations, infographics               │  │
│  • Logo animation                                    │  │
│  • Compositing tasks (rotoscope, keying)             │  │
│  OUTPUT → motion_graphics_plan                       │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│      NODE 06: Sound Design Architect (4-Layer)       │  │
│  • Layer 1: Ambiance (background atmosphere)         │  │
│  • Layer 2: Essentials (core subject sounds)         │  │
│  • Layer 3: SFX (whooshes, risers, bass drops)       │  │
│  • Layer 4: Hits & Impacts (cinematic punctuation)   │  │
│  • Music integration notes                           │  │
│  OUTPUT → sound_design_plan                          │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│        NODE 07: Audio Mixing & Mastering             │  │
│  • Track layout & sub-mix architecture               │  │
│  • Per-track processing chains (EQ, reverb, comp)    │  │
│  • Level map (dB per section)                        │  │
│  • Panning & spatial design                          │  │
│  • Ducking automation                                │  │
│  • Master chain & loudness target                    │  │
│  OUTPUT → mixing_plan                                │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│          NODE 08: Color Grading & Finishing           │  │
│  • Color correction (normalize all clips)            │  │
│  • Creative grade (temperature, contrast, sat)       │  │
│  • Finishing (grain, vignette, sharpen)               │  │
│  • Overlay placement (mattes, light leaks)           │  │
│  • Export settings                                   │  │
│  OUTPUT → color_plan                                 │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│             NODE 09: Self-Critique                   │  │
│  • 8-dimension audit (workflow, cuts, effects,       │  │
│    motion graphics, sound, mixing, color, coherence) │  │
│  • Issue identification & fixes                      │  │
│  • Grading (A+ through D)                            │  │
│  OUTPUT → critique_report, critique_grade            │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
               ┌──────────────┐                          │
               │  CONDITION   │                          │
               │  Grade ≥ A?  │                          │
               └──────┬───────┘                          │
                 YES  │  NO (& revision_count < 2)       │
                      │  └───────────────────────────────┘
                      ▼           (loop back to node 04)
┌─────────────────────────────────────────────────────┐
│          NODE 10: Final Execution Package             │
│  • Compiles ALL plans into single document           │
│  • 12-section editor handoff package                 │
│  • Step-by-step workflow (26 steps)                  │
│  • Time estimate per phase                           │
│  OUTPUT → execution_package                          │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
                  END NODE
            Returns: execution_package
```

---

## Flow State Variables Reference

| Variable | Set By | Used By | Description |
|----------|--------|---------|-------------|
| `preplanning_package` | Start Node | Node 02 | Raw input from preplanning pipeline |
| `project_brief` | Node 02 | Nodes 03-10 | Extracted project brief |
| `storyboard` | Node 02 | Nodes 03-10 | Extracted storyboard |
| `pacing_map` | Node 02 | Nodes 03, 06, 07 | Extracted pacing/rhythm map |
| `creative_strategy` | Node 02 | Nodes 03-08 | Extracted creative strategy |
| `software_suite` | Start Node | Node 02 | Editor's software choice |
| `editor_skill_level` | Start Node | Nodes 02, 04, 05 | Skill-adaptive instructions |
| `available_plugins` | Start Node | Node 04 | Plugin availability for alternatives |
| `asset_plan` | Node 02 | Nodes 03, 09 | File structure + sourcing plan |
| `first_cuts_plan` | Node 03 | Nodes 04, 06, 09 | Assembly strategy |
| `effects_plan` | Node 04 | Nodes 05, 08, 09 | Per-shot effects + transitions |
| `motion_graphics_plan` | Node 05 | Node 09 | Text, callouts, logo animation |
| `sound_design_plan` | Node 06 | Nodes 07, 09 | 4-layer sound blueprint |
| `mixing_plan` | Node 07 | Node 09 | Audio engineering plan |
| `color_plan` | Node 08 | Node 09 | Color + finishing plan |
| `critique_report` | Node 09 | Node 10 | Audit results |
| `critique_grade` | Node 09 | Condition | Grade for routing |
| `revision_count` | Node 09 | Condition | Loop counter (max 2) |
| `execution_package` | Node 10 | End Node | Final compiled output |

---

## Workshop Technique Mapping

| Workshop | Techniques Extracted | Used In Node(s) |
|----------|---------------------|-----------------|
| **Level 8 (F1 Ad)** | Script → cuts workflow, match cuts, flash transitions, mask transitions, 3D effects, 4-layer sound design, audio mixing, logo animation | Nodes 03, 04, 05, 06, 07, 08 |
| **Level 9 (Infographics)** | Brief analysis, visual feeding, 3D text/tracking, motion tracking, callouts/masks, logo via tracking | Nodes 02, 05 |
| **Level 10 (Trendy Effects)** | 3D camera transitions, mask transitions, speed ramp transitions, rotoscoping, cyber effects, turbulent displace, glow, posterize time | Nodes 04, 05 |
| **Level 11 (Speed Ramp)** | Speed ramp graph editor, CC Force Motion Blur, particle systems, anchor point rotation, pre-compose workflow | Node 04 (partially), Node 08 |

---

## Model Recommendations

| Node | Token Intensity | Recommended Model |
|------|----------------|-------------------|
| 02: Asset Organization | Low-Medium | Any model (GPT-4o-mini, Sonnet) |
| 03: First Cuts | Medium | Claude Sonnet 4 / Gemini 2.5 Pro |
| 04: Effects Designer | **High** | Claude Sonnet 4 / Gemini 2.5 Pro (100K+ context) |
| 05: Motion Graphics | Medium-High | Claude Sonnet 4 / Gemini 2.5 Pro |
| 06: Sound Design | **High** | Claude Sonnet 4 / Gemini 2.5 Pro (100K+ context) |
| 07: Audio Mixing | Medium | Claude Sonnet 4 / Gemini 2.5 Pro |
| 08: Color Finishing | Low-Medium | Any model |
| 09: Self-Critique | **Very High** | Claude Sonnet 4 / Gemini 2.5 Pro (receives ALL state) |
| 10: Execution Package | **Very High** | Claude Sonnet 4 / Gemini 2.5 Pro (compiles everything) |
