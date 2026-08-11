# Node 01: Start / Intake (Viral Flow)

> **Node Type**: Start Node (Form Input)
> **Writes to**: Multiple flow state variables
> **Purpose**: Receives the pre-planning package and collects viral-edit-specific inputs.

---

## Form Fields

### Required Fields

| Field Name | Field ID | Type | Options/Notes |
|-----------|----------|------|---------------|
| Pre-Planning Package | `preplanningPackage` | Text (multiline) | Full output from Video Pre-Planning Pipeline |
| Clip Count | `clipCount` | Number | How many source clips will be used |
| Clip Descriptions | `clipDescriptions` | Text (multiline) | Brief description of each clip (content, duration, frame rate) |
| Target Duration | `targetDuration` | Select | `15 seconds`, `30 seconds`, `45 seconds`, `60 seconds` |
| Music Track BPM | `musicBPM` | Number | BPM of the selected music |
| Music Drop Timestamps | `musicDrops` | Text | Comma-separated timestamps of music drops/beats (e.g., "0:03, 0:08, 0:15, 0:22") |

### Optional Fields

| Field Name | Field ID | Type | Options/Notes |
|-----------|----------|------|---------------|
| Source Frame Rate | `sourceFrameRate` | Select | `24fps`, `30fps`, `60fps`, `120fps`, `Mixed` |
| Trend Style | `trendStyle` | Text | Describe the viral trend you're following (if any) |
| Reference Videos | `referenceVideos` | Text (multiline) | Links to viral edits you want to emulate |
| Available Plugins | `availablePlugins` | Text | List of AE plugins available |

---

## Flow State Initialization

```json
{
  "preplanning_package": "{{ $form.preplanningPackage }}",
  "project_brief": "",
  "storyboard": "",
  "pacing_map": "",
  "creative_strategy": "",
  "clip_count": "{{ $form.clipCount }}",
  "clip_descriptions": "{{ $form.clipDescriptions }}",
  "target_duration": "{{ $form.targetDuration }}",
  "music_bpm": "{{ $form.musicBPM }}",
  "music_drops": "{{ $form.musicDrops }}",
  "source_framerate": "{{ $form.sourceFrameRate }}",
  "trend_style": "{{ $form.trendStyle }}",
  "reference_videos": "{{ $form.referenceVideos }}",
  "available_plugins": "{{ $form.availablePlugins }}",
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

## Notes

- **Frame rate is critical**: Speed ramping quality depends heavily on source frame rate. 60fps+ is ideal. 24fps will look choppy in slow-motion. The system will adapt recommendations based on this.
- **Music BPM drives everything**: In viral edits, cuts and speed ramps sync to the beat. Knowing the BPM enables precise timing calculations.
- **Music drop timestamps**: These are the key moments where speed ramp peaks and visual impacts should land.
