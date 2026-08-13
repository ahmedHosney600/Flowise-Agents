# Complete Study & Testing Guide for the 3 Video Editing Brain Workflows

This guide provides an end-to-end breakdown of the three Flowise AgentFlow V2 JSON workflows in this project, performs a structural audit against Flowise engine rules, and provides a complete testing framework with real example video scenarios (derived from the included **Elgendy Academy Workshops**).

---

## 1. System Overview & The 3 Workflows

The system acts as an **AI Production & Post-Production Assistant Brain** for video editors, directors, and content creators. It bridges the gap between high-level creative ideas and granular, timeline-ready execution in **Adobe Premiere Pro** and **After Effects**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AI VIDEO ASSISTANT BRAIN                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
           ┌───────────────────────────────────────────────────┐
           │ [WORKFLOW 0] Video Pre-Planning Pipeline v3       │
           │ (Video_Pre_Planning_Pipeline_v3.json)             │
           │ Role: Creative Strategy, Storyboard, Retention,   │
           │       Pacing Map & Sound Design Direction         │
           └─────────────────────────┬─────────────────────────┘
                                     │
                        Produces Pre-Planning Package
                                     │
               ┌─────────────────────┴─────────────────────┐
               ▼                                           ▼
┌───────────────────────────────┐     ┌─────────────────────────────────┐
│ [WORKFLOW 1]                  │     │ [WORKFLOW 2]                    │
│ Post-Production Execution     │     │ Speed Ramp & Viral Edit Flow    │
│ (Post_Production_Execution_   │     │ (Speed_Ramp_Viral_Flow_v1.json) │
│  Flow_v1.json)                │     │                                 │
│ For: ALL STANDARD PROJECTS    │     │ For: SHORT-FORM / VIRAL EDITS   │
│ (Ads, YouTube, Corporate,     │     │ (Reels/TikTok/Shorts, action    │
│  Infographics, Documentaries) │     │  montages, sports, car edits)   │
│ Timeline cuts, 4-layer audio, │     │ AE Graph Editor speed curves,   │
│ 3D text tracking, color LUTs  │     │ mask transitions, viral effects │
└───────────────────────────────┘     └─────────────────────────────────┘
```

---

### Deep Dive into Each Workflow

### 1. Workflow 0: Video Pre-Planning Pipeline (`Video_Pre_Planning_Pipeline_v3.json`)
* **Location**: [Video_Pre_Planning_Pipeline_v3.json](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/00_flowise_video_preplanning_flow/Video_Pre_Planning_Pipeline_v3.json)
* **Purpose**: Generates the complete creative blueprint before touching any editing software.
* **Nodes (15 total)**:
  1. `startAgentflow_0` (Start Intake Form): Collects 25 project fields (topic, goal, target duration, platform, tone, audience, visual style, etc.).
  2. `llmAgentflow_0` (Brief Builder): Synthesizes intake into a unified Project Brief.
  3. `humanInputAgentflow_0` (Review Brief Gate): Pauses execution for human approval/feedback.
  4. `llmAgentflow_1` (Creative Strategy): Visual mood, reference films, color palette, editing style.
  5. `llmAgentflow_2` (Narrative Structure): 3-act / hook-story-offer storytelling arc, open loops.
  6. `llmAgentflow_3` (Retention Engineer): Pattern interrupts every 3–5 seconds, drop-off fixes.
  7. `llmAgentflow_4` (Storyboard Builder): Shot-by-shot storyboard with visual framing and sound cues.
  8. `llmAgentflow_5` (Pacing & Rhythm): Beat map, energy curve, silence placement.
  9. `llmAgentflow_6` (Self-Critique Audit): Evaluates quality and assigns grade (`A+`, `A`, `B`, `C`, `D`).
  10. `conditionAgentflow_0` & `conditionAgentflow_1`: Grade check and loop guard (max 2 revisions).
  11. `llmAgentflow_7` / `llmAgentflow_8`: QA & Final Pre-Planning Package compiler.
  12. `directReplyAgentflow_0`: Formats and delivers the package to the user.

---

### 2. Workflow 1: Post-Production Execution Flow (`Post_Production_Execution_Flow_v1.json`)
* **Location**: [Post_Production_Execution_Flow_v1.json](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/01_post_production_execution_flow/Post_Production_Execution_Flow_v1.json)
* **Purpose**: Converts the pre-planning package into a timeline execution plan (based on Workshop Level 8 F1 Ad & Level 9 Infographics).
* **Nodes (17 total)**:
  1. `startAgentflow_0` (Start): Ingests pre-planning package + footage specs + editing suite.
  2. `llmAgentflow_0` (Asset Organization): File tree (`01_VO`, `02_Footage`, `03_Music`, `04_SFX`, `05_GFX`), footage sourcing.
  3. `humanInputAgentflow_0` (Asset Gate): Human confirms asset availability before processing downstream.
  4. `llmAgentflow_1` (First Cuts Strategist): In/out cut points, cutting on music beats, J/L cuts.
  5. `llmAgentflow_2` (Effects & Transition Designer): Whip pans, mask wipes, zoom transitions, rotoscoping.
  6. `llmAgentflow_3` (Motion Graphics Planner): 3D text tracking, HUD callouts, lower thirds, logo reveals.
  7. `llmAgentflow_4` (Sound Design Architect): 4-layer audio system (**Layer 1: Ambiance**, **Layer 2: Essentials/Foley**, **Layer 3: SFX/Whooshes**, **Layer 4: Hits & Impacts**).
  8. `llmAgentflow_5` (Audio Mixing & Mastering): Track mixer levels (VO: -6 to -12 dB, Music: -18 to -24 dB, SFX: -12 to -15 dB, Hits: -3 dB limiter), EQ & reverb.
  9. `llmAgentflow_6` (Color Grading & Finishing): LUT selection, contrast curves, film grain, letterboxing.
  10. `llmAgentflow_7` (Self-Critique Audit): Fast audit without modifying state.
  11. `llmAgentflow_8` (Revision Applier - Lazy): Only runs if critique fails.
  12. `conditionAgentflow_0` & `conditionAgentflow_1`: Dual-condition loop guard with escape path.
  13. `llmAgentflow_9` / `llmAgentflow_10`: Compiles the master Editor Handoff Package.

---

### 3. Workflow 2: Speed Ramp & Viral Edit Flow (`Speed_Ramp_Viral_Flow_v1.json`)
* **Location**: [Speed_Ramp_Viral_Flow_v1.json](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/new%20flows/02_speed_ramp_viral_flow/Speed_Ramp_Viral_Flow_v1.json)
* **Purpose**: High-energy short-form video brain (based on Workshop Level 10 & Level 11 Viral Speed Ramp).
* **Nodes (12 total)**:
  1. `startAgentflow_0` (Start): Clip durations, framerate (60fps/120fps), music BPM and drop timestamps.
  2. `llmAgentflow_0` (Clip Arrangement): High-impact sequence order.
  3. `llmAgentflow_1` (Speed Ramp Designer): After Effects Graph Editor speed curves (e.g. 500% speed-up -> 30% slow-mo on impact with Optical Flow).
  4. `llmAgentflow_2` (Viral Effects & Transitions): Turbulent Displace, Directional Blur, Cyber glitch, RGB split, mask zoom.
  5. `llmAgentflow_3` (Sound Design & Finishing): Whoosh risers, sub drops, impact hits synced with speed ramp peaks, glow and CC finishing.
  6. `llmAgentflow_4` (Self-Critique Audit) & `llmAgentflow_5` (Revision Applier).
  7. `conditionAgentflow_0` & `conditionAgentflow_1` (Grade check & loop guard).
  8. `llmAgentflow_6` (Final Viral Package) & `directReplyAgentflow_0` (Output).

---

## 2. Technical Audit & Bug Report (Flowise Rules)

During our automated static analysis of the 3 JSON files against [mustread_flowise_instructions.md](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/mustread_flowise_instructions.md), here are the findings:

### ⚠️ Critical Finding: Flow 2 Rule 1 Violation (Condition Fan-in)
> [!WARNING]
> **Bug in `Speed_Ramp_Viral_Flow_v1.json`**:
> `Final Viral Package` (`llmAgentflow_6`) receives incoming connections from **both** `conditionAgentflow_0` and `conditionAgentflow_1`.
> In Flowise AgentFlow V2, when two condition nodes fan directly into the same node, **the flow silently halts at runtime with an empty output**.

```
Current Flow 2 (Buggy):
[Grade Check (Cond 0)] ────True────► [Final Viral Package (llmAgentflow_6)] ──► [Output]
      │ False                                      ▲
      ▼                                            │
[Revision Applier] ──► [Loop Guard (Cond 1)] ─True─┘ (FAN-IN COLLISION!)

Required Fix (Same pattern as Flow 0 and Flow 1):
[Grade Check (Cond 0)] ────True────► [Final Viral Package] ────────────────────► [Output]
      │ False                                                                      ▲
      ▼                                                                            │
[Revision Applier] ──► [Loop Guard (Cond 1)] ─True─► [Final Package (Loop Escape)] ┘
```

### ℹ️ Rule 6 Notice: Local LLM Proxy Endpoint
All nodes in the 3 JSON files are pre-configured to:
`http://localhost:4981/openai/v1` (Model: `gpt-4o`).
* If you are running the local Gemini proxy server (`go run cmd/server/main.go`), ensure it is active on port `4981`.
* Alternatively, if importing into a standard Flowise instance, select your connected Flowise Chat Model credential (e.g. Anthropic Claude 3.5 Sonnet / Gemini 1.5/2.0 Flash / OpenAI GPT-4o).

---

## 3. Step-by-Step Testing Guide with Example Data & Video

Below are test scenarios built directly from the workshop project files in `Workshops/`.

---

### 🧪 Test 1: Testing Workflow 0 (Pre-Planning Pipeline)

#### **Test Case**: Formula 1 60s Commercial ("Battle of Speed & Courage")
*Source: `Workshops/10.Level 8 ورشة إعلان Formula 1`*

#### **Step 1: Ingest Form Data into Flow 0**
When opening the Chat/Run modal in Flowise for **Workflow 0**, fill in the intake form with the following data:

```json
{
  "video_topic": "Formula 1 Racing - The Battle of Speed, Courage and Survival",
  "primary_goal": "Hype Commercial / Motivational Ad showcasing the extreme mental and physical warfare of F1 drivers",
  "core_message": "Formula 1 is not just driving fast; it is a battle where 20 drivers risk everything at 350 km/h.",
  "content_type": "Commercial / Brand Ad",
  "target_duration": "60 seconds",
  "target_audience": "Motorsport fans, adrenaline seekers, sports apparel audience (18-35)",
  "primary_platform": "YouTube / Instagram Reels / TV Broadcast",
  "video_tone": "Epic, dramatic, intense, cinematic, high-adrenaline",
  "brand_name": "Formula 1",
  "visual_references": "Nike commercial style, fast kinetic match cuts, archive grainy vintage footage transitioning to 4K modern telemetry footage",
  "audio_references": "Hans Zimmer cinematic hybrid orchestral track, building ticking clock, visceral V10 and turbo-hybrid engine roars, team radio chatter",
  "key_scenes": "1. Silence before the green lights (driver heartbeat). 2. Explosive start into Turn 1. 3. Rain and near-crash tension. 4. High-speed cornering at 350 km/h. 5. Victory celebration and logo reveal.",
  "cta": "Feel the Rush - Watch the Grand Prix this Sunday"
}
```

#### **Step 2: Human Approval Gate**
1. Flow will generate the **Project Brief** via `llmAgentflow_0`.
2. Execution will pause at `humanInputAgentflow_0`.
3. In the Flowise chat interface, verify the brief, type `"Approved, proceed with high-tempo kinetic pacing"`, and click **Proceed**.

#### **Step 3: Verification of Flow 0 Output**
Ensure the final output contains:
- [x] **3-Act Narrative Arc** with Hook (0–3s heartbeat), Conflict (4–40s wheel-to-wheel warfare), Climax (41–52s overtake), and Outro (53–60s).
- [x] **Shot-by-Shot Storyboard** (12–15 distinct shots with Framing, Action, Camera Movement, and Audio Stems).
- [x] **Pacing Beat Map** (Energy curve peaking at 50s, 120–140 BPM rhythm).
- [x] **Critique Score** of `A` or `A+`.

---

### 🧪 Test 2: Testing Workflow 1 (Post-Production Execution Flow)

#### **Step 1: Feed Pre-Planning Output into Flow 1**
Take the final output markdown from Test 1 (or paste the summary below) into the Start Node of **Workflow 1**:

```json
{
  "preplanning_package": "PROJECT: Formula 1 60s Ad\nTHEME: Speed, Courage & Survival\nSHOTS: 14 shots (Heartbeat intro, green lights, Turn 1 lockup, rain spray, 350km/h straight, podium champagne)\nPACING: 130 BPM building orchestral track",
  "software_suite": "Adobe Premiere Pro 2024 & Adobe After Effects 2024",
  "available_plugins": "Boris FX Sapphire, Red Giant Universe, Mister Horse, Optical Flares",
  "editor_skill_level": "Advanced",
  "target_export_spec": "4K UHD (3840x2160), 24fps, ProRes 422HQ & H.264 Web Master"
}
```

#### **Step 2: Human Asset Gate**
1. Node `02_asset_organization` will output the file folder tree (`01_VO`, `02_Footage`, `03_Music`, `04_SFX`, `05_GFX`).
2. The Human Input gate will prompt: Select `"Continue to first cuts"`.

#### **Step 3: Verification of Flow 1 Output**
Verify that the generated Execution Blueprint contains:
- [x] **First Cuts Blueprint**: Specific In/Out markers, beat-synced cuts on the downbeats (0:03.12, 0:06.24, 0:09.18), J-cut audio lead-ins for engine sounds.
- [x] **Effects & Transitions Plan**: Match cut on tire spin to wheel rim, directional whip pans with 180° shutter motion blur, masked speed transitions through tire smoke.
- [x] **Motion Graphics Plan**: 3D camera tracked speedometer and telemetry HUD over the car cockpit in After Effects; metallic 3D F1 logo reveal.
- [x] **4-Layer Sound Design Blueprint**:
  - *Layer 1 (Ambiance)*: Grandstand crowd murmur, track wind, distant exhaust hum (-22 dB).
  - *Layer 2 (Essentials)*: Gear shifts, tire squeal, engine RPM revving (-12 dB).
  - *Layer 3 (SFX)*: Deep sub-bass whooshes on camera fly-bys, riser tension swells (-14 dB).
  - *Layer 4 (Hits & Impacts)*: Sub-boom on the 5 green lights turning on, metallic smash on crash near-miss (-3 dB).
- [x] **Audio Track Mixer Spec**: Strict dB levels matching the workshop guidelines.
- [x] **Color Grading & Finishing**: Kodak 2383 film print emulation LUT, 35mm grain at 15% opacity, vignette at -0.4.

---

### 🧪 Test 3: Testing Workflow 2 (Viral Speed Ramp Flow)

#### **Test Case**: 20s High-Energy Supercar / Drift Edit
*Source: `Workshops/13.Level 11 After Effects Viral Speed Ramp Workshop`*

#### **Step 1: Ingest Viral Edit Data into Flow 2**
Paste the following input into the Start Node of **Workflow 2**:

```json
{
  "clip_descriptions": "Clip 1: Driver putting helmet on (Close Up, 60fps).\nClip 2: Exhaust fire backfire on rev (Macro, 120fps).\nClip 3: Car launching from standstill with tire smoke (Wide low angle, 60fps).\nClip 4: High-speed drift cornering around apex (Tracking gimbal shot, 120fps).\nClip 5: Drone chase flying 1 meter above the rear spoiler (FPV, 60fps).\nClip 6: Car stopping inches from camera, driver staring through windshield (Front Wide, 60fps).",
  "music_bpm": "135 BPM (Aggressive Phonk / Trap Instrumental)",
  "music_drops": "Drop 1 at 0:02.80, Drop 2 at 0:07.40, Main Bass Drop at 0:12.60, Final Hit at 0:18.20",
  "source_framerate": "60fps and 120fps",
  "target_duration": "20 seconds",
  "viral_platform": "TikTok / Instagram Reels (9:16 vertical)",
  "desired_vibe": "Ultra-fast speed ramping, trendy mask wipes, turbulent displacement transitions, heavy bass hits"
}
```

#### **Step 2: Verification of Flow 2 Output**
Verify that the output provides exact After Effects execution values:
- [x] **Graph Editor Curve Specifications**:
  - *Clip 1 -> Clip 2*: Normal speed 100% -> Fast ramp 600% (frames 45–55) -> Snap to 25% slow-mo with **Optical Flow** at 0:02.80 bass drop.
  - Velocity bezier handles (e.g. *Ease Out 85%, Ease In 90%*).
- [x] **VFX Stack**:
  - Turbulent Displace (Size: 15, Amount: 35 keyframed across 4 frames) on transition points.
  - CC Force Motion Blur / Directional Blur (Angle matching car drift vector).
  - Chromatic aberration and RGB split on bass drops.
- [x] **Sound Design Sync**:
  - Heavy bass drops aligned down to the exact millisecond timestamps (`0:02.80`, `0:07.40`, `0:12.60`).
  - Suction / reverse whoosh 0.5s prior to each speed burst.

---

## 4. How to Test Inside Flowise (Quick Checklist)

1. **Verify Backend LLM Proxy**:
   - Make sure your local API endpoint or API keys are active.
   - If using local proxy: check that `http://localhost:4981/openai/v1` is responding.

2. **Import the JSON files**:
   - In Flowise UI: Click **AgentFlows** -> **Import Flow** -> Select the `.json` file.

3. **Check Connection Handles**:
   - Inspect the Condition node handles (`conditionAgentflow_0` and `conditionAgentflow_1`).
   - In Flow 2, apply the loop escape duplicate node if you plan on testing sub-A revision loops.

4. **Execute with the Test Cases above**:
   - Click the chat bubble icon in Flowise.
   - Submit the test payload.
   - Inspect the state variables in the Flowise runtime debug inspector to ensure every node writes to its designated `$flow.state` key.

---

## 5. Summary Table of the 3 Workflows

| Feature | Workflow 0 (Pre-Planning) | Workflow 1 (Post-Production) | Workflow 2 (Viral Speed Ramp) |
| :--- | :--- | :--- | :--- |
| **File** | [Video_Pre_Planning_Pipeline_v3.json](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/00_flowise_video_preplanning_flow/Video_Pre_Planning_Pipeline_v3.json) | [Post_Production_Execution_Flow_v1.json](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/01_post_production_execution_flow/Post_Production_Execution_Flow_v1.json) | [Speed_Ramp_Viral_Flow_v1.json](file:///Users/ahmedmac/Desktop/My%20Computer/Programming%20Proejcts/Prompt%20Storytelling%20System/new%20flows/02_speed_ramp_viral_flow/Speed_Ramp_Viral_Flow_v1.json) |
| **Stage** | Pre-Production | Post-Production (Standard) | Post-Production (Viral Short-Form) |
| **Target Video** | Any video concept | Ads, YouTube, Corporate, GFX | TikTok/Reels Action & Montages |
| **Primary Tools** | Creative Strategy & Storyboarding | Premiere Pro & After Effects | After Effects (Graph Editor) |
| **Audio Strategy** | Music style & pacing guidelines | 4-layer audio stems & mixing | Beat-synced SFX & heavy drops |
| **Key Output** | Shot-by-shot storyboard + beat map | Complete editor timeline blueprint | Speed graph curves + VFX stack |

Would you like me to apply the structural fix to `Speed_Ramp_Viral_Flow_v1.json` to resolve the Condition Fan-in issue, or help you run an automated test simulation against your active local model?