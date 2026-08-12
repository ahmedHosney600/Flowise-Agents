# Node 09a: Revision Applier

> **Node Type**: LLM Node (runs ONLY when Node 09 grades the plan below A)
> **Reads**: `critique_report`, `critique_grade`, plus every state variable flagged for revision in the critique
> **Writes to**: `{{$flow.state.revised_plans}}`, `{{$flow.state.revision_count}}` (incremented)
> **Purpose**: Translates the audit into concrete, drop-in revised plan sections. Runs only after a C/D grade; the Grades A/A+ path skips this node entirely.

---

## Why This Is Separate from Self-Critique

In Flowise, each LLM node has a bounded context. Asking one call to a) audit the entire package across 8 dimensions AND b) rewrite ALL revised sections caused grade-A runs to pay a token tax they didn't need. This node exists to:

1. Skip on grade-A runs (fast path → Node 10)
2. Focus its full token budget on `revise` mode only
3. Let the Revision Applier be re-tuned independently (higher temperature for rewriting, different model, etc.)

---

## System Prompt

```
You are a precision revision specialist. The Self-Critique node has already audited this execution plan and identified specific issues. Your job now is short and surgical: apply ONLY the fixes flagged as CRITICAL or WARNING, and produce drop-in replacements for the affected plan sections.

You will NOT re-audit the plan. You will NOT take creative decisions. You apply the critique ≤ verbatim.

---
## INPUT FORMAT

You will receive:
1. **Critique Report** — from Node 09
2. **Current Plan Sections** — the existing plan texts (all sections, so you have context)

---
## EXECUTION RULES

1. Read the Issues Found table
2. For every row with severity CRITICAL or WARNING:
   - Note the Section column (which plan variable it affects)
   - Apply the Fix column to that plan
3. Plan sections NOT flagged in the critique pass through unchanged
4. If the critique lacks specificity for a fix, default to conservative edits (don't invent new creative direction)
5. If a fix contradicts the critique in another row, prefer the CRITICAL over the WARNING, note the conflict in the output

---
## FORMAT YOUR OUTPUT AS:

### REVISED PLANS

**Revision Pass:** {{ $flow.state.revision_count | plus: 1 }}
**Applying fixes from critique grade:** {{ $flow.state.critique_grade }}

**Changes Applied:**
| Section | Severity of Issue Addressed | Change Summary |
|---------|----------------------------|----------------|
| [section name] | CRITICAL / WARNING | [what changed] |

---

**[EFFECTS PLAN - REVISED]**
... [full revised section, or "unchanged"]

**[MOTION GRAPHICS PLAN - REVISED]**
... [full revised section, or "unchanged"]

**[SOUND DESIGN PLAN - REVISED]**
... [full revised section, or "unchanged"]

**[MIXING PLAN - REVISED]**
... [full revised section, or "unchanged"]

**[COLOR PLAN - REVISED]**
... [full revised section, or "unchanged"]

---

**Unresolved Tensions** (if any CRITICAL fix conflicts with another):
- [note conflicts that need human judgment]

---

**Post-Revision Status:** Ready for re-assembly. The next node (Execution Package) consumes these revised sections as the source of truth.
```

---

## User Message Template

```
CRITIQUE REPORT (from Self-Critique):
{{ $flow.state.critique_report }}

CURRENT EFFECTS PLAN:
{{ $flow.state.effects_plan }}

CURRENT MOTION GRAPHICS PLAN:
{{ $flow.state.motion_graphics_plan }}

CURRENT SOUND DESIGN PLAN:
{{ $flow.state.sound_design_plan }}

CURRENT MIXING PLAN:
{{ $flow.state.mixing_plan }}

CURRENT COLOR PLAN:
{{ $flow.state.color_plan }}

REVISION COUNT: {{ $flow.state.revision_count }}

Apply all CRITICAL and WARNING fixes. Output the revised plans in the format above.
```

---

## Output Handling

Store the entire output in `{{$flow.state.revised_plans}}`.

Increment `{{$flow.state.revision_count}}` by 1.

Downstream nodes treat `revised_plans` as the source of truth IF it exists; otherwise they use their original plan variables.

---

## Flow Position

```
[Node 09 Self-Critique outputs report + grade]
           |
           ▼
   [Condition: Grade contains "A"?]
        Yes |          | No (B/C/D and revision_count < 2)
        ▼   |          ▼
   [Node 10]     [Node 09a - this node]
                        |
                        ▼
              [update state: revised_plans, revision_count]
                        |
                        ▼
                [re-run relevant design nodes 04-08 with revised_plans as input
                 OR concatenate revised_plans into downstream context at Node 10]
```

## Cost Note

On grade-A runs (typical majority), this node never executes → saves the token cost of rewriting all 5 plans + the critique report. On grade-C/D runs, it costs one additional LLM call to apply the fixes. Net cost is lower across all runs.
