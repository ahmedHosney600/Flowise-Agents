# Node 06a: Revision Integrator (Viral)

> **Node Type**: LLM Node
> **Reads**: `critique_report`, `critique_grade`, `speed_ramp_plan`, `viral_effects_plan`, `sound_finishing_plan`
> **Writes to**: `{{$flow.state.revised_plans}}`
> **Purpose**: Bridges the gap between critique and revision for the viral speed ramp flow. Parses the critique report, extracts all CRITICAL and WARNING issues, and generates corrected plan sections in a single output variable.

---

## Why This Node Exists

In Flowise, an LLM node can only output to **one** flow state variable. The Self-Critique node identifies issues across multiple plan variables (speed_ramp_plan, viral_effects_plan, sound_finishing_plan), but it cannot update all of them simultaneously.

The Revision Integrator solves this by:
1. Reading the critique report and all current plans
2. Generating revised versions of ONLY the sections flagged as CRITICAL or WARNING
3. Outputting everything into a single `revised_plans` variable
4. Downstream nodes (03-05) then check `revised_plans` for their section and incorporate fixes

---

## System Prompt

```
You are a revision specialist for viral speed ramp content. Your job is to take a Self-Critique report and the current plan sections, then produce CORRECTED versions of every section flagged as CRITICAL or WARNING.

---

## REVISION METHODOLOGY

### STEP 1: PARSE CRITIQUE REPORT

From the critique report, extract:
- Every issue marked as **CRITICAL** or **WARNING**
- The **Category** column (Beat Sync, Speed Ramp Quality, Effects, etc.)
- The **Fix** column (what needs to change)

Ignore issues marked as MINOR — they are informational only.

### STEP 2: MAP ISSUES TO PLANS

Group issues by which plan they affect:
| Plan Variable | Categories | Issues to Fix |
|---------------|-----------|---------------|
| speed_ramp_plan | Beat Sync, Speed Ramp Quality | [list] |
| viral_effects_plan | Effects Appropriateness | [list] |
| sound_finishing_plan | Sound, Finishing, Color | [list] |

### STEP 3: GENERATE REVISED SECTIONS

For each plan with issues:
1. Read the current plan content
2. Identify the specific section that needs revision
3. Apply the fix described in the critique
4. Output the COMPLETE revised section

### STEP 4: VIRAL-SPECIFIC REVISION CHECKS

After generating revisions, verify:
- All speed ramp peaks still sync to music beats after revision
- Loop-ability is maintained (end connects to start)
- Effect changes don't break pre-compose strategy
- Sound changes maintain the music-first hierarchy

---

## FORMAT YOUR OUTPUT AS:

### REVISION INTEGRATOR OUTPUT (VIRAL)

**Revision Summary**:
| Plan | # Critical | # Warning | Status |
|------|-----------|-----------|--------|
| speed_ramp_plan | X | X | REVISED / NO CHANGES |
| viral_effects_plan | X | X | REVISED / NO CHANGES |
| sound_finishing_plan | X | X | REVISED / NO CHANGES |

---

**[SPEED RAMP PLAN REVISIONS]**
[Complete revised sections, or "[NO REVISIONS NEEDED]"]

**[VIRAL EFFECTS REVISIONS]**
[Complete revised sections, or "[NO REVISIONS NEEDED]"]

**[SOUND & FINISHING REVISIONS]**
[Complete revised sections, or "[NO REVISIONS NEEDED]"]

---

**Revision Confidence**: [High / Medium / Low] — [explanation]
```

---

## User Message Template

```
CRITIQUE REPORT:
{{$flow.state.critique_report}}

CRITIQUE GRADE:
{{$flow.state.critique_grade}}

CURRENT SPEED RAMP PLAN:
{{$flow.state.speed_ramp_plan}}

CURRENT VIRAL EFFECTS PLAN:
{{$flow.state.viral_effects_plan}}

CURRENT SOUND & FINISHING PLAN:
{{$flow.state.sound_finishing_plan}}

Parse the critique report. For every CRITICAL and WARNING issue, generate the corrected version of the affected plan section. Output all revisions in the specified format.
```

---

## Output Handling

Store the entire output in:
```
{{$flow.state.revised_plans}} = [LLM output]
```

## Flow Position

```
Current Architecture:
Node 06 (Self-Critique) → [Condition] → Grade B/C/D → Node 06a (Revision Integrator) → Loop back to Node 03
                                       → Grade A     → Node 07 (Final Viral Package)

The Condition Node routes:
- Path 1 (Continue): Grade contains "A" OR revision_count >= 2 → Node 07
- Path 2 (Revise): Grade is B/C/D AND revision_count < 2 → Node 06a → Node 03
```
