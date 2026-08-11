# Node 01: Start / Intake

> **Node Type**: Start Node (Form Input)
> **Writes to**: Multiple flow state variables
> **Purpose**: Receives the completed pre-planning package and collects project-specific execution inputs.

---

## Form Fields

### Required Fields

| Field Name | Field ID | Type | Options/Notes |
|-----------|----------|------|---------------|
| Pre-Planning Package | `preplanningPackage` | Text (multiline) | Paste the full output from the Video Pre-Planning Pipeline |
| Software Suite | `softwareSuite` | Select | `Premiere Pro + After Effects`, `DaVinci Resolve + Fusion`, `Final Cut Pro + Motion`, `Premiere Pro Only`, `After Effects Only` |
| Editor Skill Level | `editorSkillLevel` | Select | `Beginner (basic cuts and effects)`, `Intermediate (comfortable with keyframes and masking)`, `Advanced (3D tracking, expressions, complex compositing)`, `Expert (plugin development, scripting)` |
| Available Plugins | `availablePlugins` | Text (multiline) | List any plugins/presets the editor has (e.g., Sapphire, Red Giant, Motion Bro, Film Impact) |

### Optional Fields

| Field Name | Field ID | Type | Options/Notes |
|-----------|----------|------|---------------|
| Footage Frame Rate | `footageFrameRate` | Select | `23.976fps`, `24fps`, `25fps`, `29.97fps`, `30fps`, `50fps`, `60fps`, `120fps`, `Mixed` |
| Footage Resolution | `footageResolution` | Select | `720p`, `1080p`, `2K`, `4K`, `Mixed` |
| Stock Footage Sources | `stockSources` | Text | Where to source stock (YouTube channels, stock libraries, client-provided) |
| AI Tools Available | `aiTools` | Text | E.g., ElevenLabs for VO, Midjourney for stills, Runway for generation |
| Deadline Pressure | `deadlinePressure` | Select | `No rush — quality first`, `Standard turnaround`, `Tight deadline — efficient workflow`, `Rush — fastest possible` |
| Music Track BPM | `musicBPM` | Number | If music is already selected, provide BPM |
| Music Track Link | `musicTrackLink` | Text | Link or name of selected music track |

---

## Flow State Initialization

```json
{
  "preplanning_package": "{{ $form.preplanningPackage }}",
  "project_brief": "",
  "storyboard": "",
  "pacing_map": "",
  "creative_strategy": "",
  "narrative_structure": "",
  "retention_map": "",
  "software_suite": "{{ $form.softwareSuite }}",
  "editor_skill_level": "{{ $form.editorSkillLevel }}",
  "available_plugins": "{{ $form.availablePlugins }}",
  "footage_framerate": "{{ $form.footageFrameRate }}",
  "footage_resolution": "{{ $form.footageResolution }}",
  "asset_plan": "",
  "first_cuts_plan": "",
  "effects_plan": "",
  "motion_graphics_plan": "",
  "sound_design_plan": "",
  "mixing_plan": "",
  "color_plan": "",
  "critique_report": "",
  "critique_grade": "",
  "revision_count": 0,
  "execution_package": ""
}
```

---

## Notes

- The `preplanningPackage` field accepts the complete output from the Video Pre-Planning Pipeline (all phases compiled).
- The system will automatically parse the project brief, storyboard, pacing map, and creative strategy from the preplanning package in Node 02.
- If the editor has a tight deadline, later nodes will suggest simpler effect alternatives and streamlined workflows.
- If the editor skill level is Beginner, complex techniques (3D tracking, expressions) will be replaced with simpler alternatives.
