# Speed Ramp & Viral Edit Flow — System Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    START NODE (Form Input)                    │
│  Receives: Pre-planning package + clip info + music BPM      │
│  Initializes: All flow state variables                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│            NODE 02: Clip Arrangement & Selection             │
│  • Analyzes each clip for speed ramp potential               │
│  • Maps music beat grid from BPM                             │
│  • Plans clip order synced to music structure                │
│  • Selects in/out points and peak frames                     │
│  • Designs energy flow pattern                               │
│  OUTPUT → clip_arrangement                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│            NODE 03: Speed Ramp Designer             ◄──┐     │
│  • Designs exact speed ramp curves per clip             │     │
│  • Frame rate constraint analysis                       │     │
│  • Graph editor keyframe specifications                 │     │
│  • Beat-to-speed sync table                             │     │
│  • Motion blur integration points                       │     │
│  OUTPUT → speed_ramp_plan                               │     │
└─────────────────────┬──────────────────────────────────│────┘
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│          NODE 04: Viral Effects & Transitions         │  │
│  • Speed-through and whip pan transitions            │  │
│  • Turbulent displace at peaks                       │  │
│  • Subject isolation + background effects            │  │
│  • Glow, RGB split, particles                        │  │
│  • Rotoscope & masking tasks                         │  │
│  • Pre-compose strategy                              │  │
│  OUTPUT → viral_effects_plan                         │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│      NODE 05: Sound Design & Finishing (Combined)    │  │
│  SOUND: Impact SFX per ramp peak, risers, whooshes   │  │
│         Silence moments, music editing notes          │  │
│  COLOR: Quick grade recipe, clip matching             │  │
│  FINISH: Motion blur, grain, vignette, sharpen       │  │
│  OUTPUT → sound_finishing_plan                       │  │
└─────────────────────┬───────────────────────────────┘  │
                      │                                  │
                      ▼                                  │
┌─────────────────────────────────────────────────────┐  │
│             NODE 06: Self-Critique                   │  │
│  • Beat sync audit                                   │  │
│  • Speed ramp quality audit                          │  │
│  • Effects appropriateness                           │  │
│  • Loop-ability check (viral critical)               │  │
│  • Viral potential score (1-10)                      │  │
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
                      ▼           (loop back to node 03)
┌─────────────────────────────────────────────────────┐
│          NODE 07: Final Viral Package                │
│  • Compiles ALL plans into single document           │
│  • Step-by-step execution (26 steps)                 │
│  • Time estimate per phase                           │
│  OUTPUT → viral_package                              │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
                  END NODE
            Returns: viral_package
```

---

## Flow State Variables Reference

| Variable | Set By | Used By | Description |
|----------|--------|---------|-------------|
| `preplanning_package` | Start | Node 02 | Raw input from preplanning pipeline |
| `clip_count` | Start | Node 02 | Number of source clips |
| `clip_descriptions` | Start | Node 02 | Description of each clip |
| `target_duration` | Start | Node 02 | Target video length |
| `music_bpm` | Start | Nodes 02, 03, 05, 06 | Music tempo for beat calculations |
| `music_drops` | Start | Nodes 02, 03 | Timestamp list of music drops |
| `source_framerate` | Start | Node 03 | Source fps for slow-mo limits |
| `clip_arrangement` | Node 02 | Nodes 03, 04, 05 | Clip order + beat sync map |
| `speed_ramp_plan` | Node 03 | Nodes 04, 05, 06 | Per-clip ramp specs |
| `viral_effects_plan` | Node 04 | Nodes 05, 06 | Effects + transitions |
| `sound_finishing_plan` | Node 05 | Node 06 | Sound + color + finishing |
| `critique_report` | Node 06 | Node 07 | Audit results |
| `critique_grade` | Node 06 | Condition | Grade for routing |
| `revision_count` | Node 06 | Condition | Loop counter (max 2) |
| `viral_package` | Node 07 | End Node | Final output |

---

## Workshop Technique Mapping

| Workshop | Techniques Extracted | Used In Node(s) |
|----------|---------------------|-----------------|
| **Level 10 (Trendy Effects)** | 3D camera transitions, mask transitions, rotoscoping, cyber effects, turbulent displace, glow, posterize time | Node 04 |
| **Level 11 (Speed Ramp)** | Clip arrangement, speed ramp graph editor, frame rate handling, CC Force Motion Blur, particles, pre-compose, anchor point rotation, finishing chain | Nodes 02, 03, 04, 05 |

---

## Key Differences from Flow 1

| Aspect | Flow 1 (Post-Production) | Flow 2 (Viral) |
|--------|------------------------|----------------|
| Duration | Any length | 15-60 seconds |
| Primary software | Premiere + AE | After Effects primary |
| Sound design | 4 layers, detailed | Simplified (SFX + music) |
| Color grading | Full Lumetri workflow | Quick grade recipe |
| Core technique | Story-driven editing | Music-driven speed ramping |
| Transitions | Story-motivated | Beat-synced |
| Effects depth | Moderate | Heavy |
| Finishing steps | Separate node | Combined with sound |
| Self-critique focus | Methodology compliance | Viral potential + loop-ability |
| Output size | Comprehensive (12 sections) | Compact (10 sections) |
