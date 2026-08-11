# Node 01: Start Node — Project Intake Form

> **Node Type**: Start Node
> **Input Type**: formInput
> **Purpose**: Collects all project information via structured form fields before any LLM processing begins.

---

## Important: Optional Fields & Smart Defaults

Most fields are **optional**. Only the 7 core fields are required (video topic, primary goal, core message, content type, target duration, target audience, primary platform). When a user leaves an optional field unanswered, the Brief Builder (Node 02) will **automatically infer a smart default** based on the project context — rather than passing raw template variables or flagging errors.

This ensures the workflow never breaks due to missing fields.

---

## Form Fields Configuration

Add each field below to the Start Node's form configuration. Fields are grouped by category for clarity, but in Flowise they appear as a flat list.

---

### PROJECT IDENTITY (All Required)

| Field Name | Variable Key | Type | Options / Placeholder | Required |
|------------|-------------|------|----------------------|----------|
| What is the video about? | `video_topic` | String (textarea) | "Describe the core topic, subject, product, or message" | **Yes** |
| Primary goal | `primary_goal` | Options (dropdown) | `Sell a product`, `Educate`, `Entertain`, `Brand awareness`, `Tell a story`, `Document an event`, `Inspire action`, `Go viral`, `Other` | **Yes** |
| Core message (one sentence) | `core_message` | String | "The single most important takeaway for the viewer" | **Yes** |
| Content type | `content_type` | Options (dropdown) | `Commercial/Ad`, `YouTube video`, `Short-form Reel/TikTok`, `Corporate/Brand video`, `Documentary`, `Music video`, `Event highlight`, `Product showcase`, `Tutorial`, `Talking head`, `Showreel`, `Short film`, `Real estate`, `Mixed media`, `Motion graphics`, `Other` | **Yes** |
| Target duration | `target_duration` | Options (dropdown) | `15 seconds`, `30 seconds`, `60 seconds`, `2 minutes`, `3-5 minutes`, `5-10 minutes`, `10+ minutes`, `Flexible` | **Yes** |

---

### AUDIENCE & PLATFORM (Mostly Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Target audience description | `target_audience` | String (textarea) | "Age range, interests, lifestyle, profession" | **Yes** | — |
| Primary platform | `primary_platform` | Options (dropdown) | `YouTube`, `TikTok`, `Instagram Reels`, `Instagram Feed`, `LinkedIn`, `Facebook`, `TV/Broadcast`, `Cinema`, `Website`, `Presentation`, `Other` | **Yes** | — |
| Secondary platform (if any) | `secondary_platform` | Options (dropdown) | `None`, `YouTube`, `TikTok`, `Instagram Reels`, `Instagram Feed`, `LinkedIn`, `Facebook`, `TV/Broadcast`, `Website`, `Other` | No | AI infers from primary platform |
| How will viewers discover this? | `discovery_method` | Options (dropdown) | `Organic search`, `Paid ads`, `Social feed scroll`, `Direct link`, `Embedded on website`, `TV broadcast`, `Mixed` | No | AI infers from platform |
| Will viewers watch with sound? | `sound_assumption` | Options (dropdown) | `Mostly sound ON`, `Mostly sound OFF`, `50/50 split` | No | AI infers from platform norms |
| Viewer mindset | `viewer_mindset` | Options (dropdown) | `Actively searching`, `Passively scrolling`, `In a meeting/presentation`, `At an event`, `Relaxing at home`, `Mixed` | No | AI infers from platform + audience |

---

### ASSETS & RESOURCES (All Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Script / voiceover status | `script_status` | Options (dropdown) | `Full script ready`, `Outline/bullet points`, `No script yet`, `Will improvise`, `Voiceover will be recorded` | No | "No script yet" |
| Visual assets available | `visual_assets` | Options (dropdown) | `Original footage (already filmed)`, `Will shoot original footage`, `Stock footage only`, `Both original + stock`, `Product photos only`, `Screen recordings`, `Graphics/animation`, `None yet` | No | "Will shoot original footage" |
| Music status | `music_status` | Options (dropdown) | `Specific track selected`, `Genre preference`, `Mood preference only`, `No preference`, `Will be composed` | No | "Mood preference only" |
| Music details (if any) | `music_details` | String | "Genre, mood, or specific track name if selected" | No | AI suggests based on vibe/content type |
| Brand guidelines? | `brand_guidelines` | Options (dropdown) | `Yes - strict guidelines`, `Yes - flexible guidelines`, `No brand guidelines`, `Personal brand` | No | "No brand guidelines" |

---

### CREATIVE DIRECTION (Mostly Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Target emotions (pick up to 3) | `target_emotions` | String | "e.g., excited, inspired, curious, amazed, amused, empowered" | No | AI infers from topic + goal + vibe |
| Desired energy / vibe | `energy_vibe` | Options (dropdown) | `High energy / fast-paced`, `Cinematic / premium`, `Calm / elegant`, `Raw / authentic`, `Playful / fun`, `Dark / moody`, `Corporate / professional`, `Mixed` | No | AI infers from content type + platform |
| Reference videos (if any) | `reference_videos` | String (textarea) | "Links or descriptions of videos you admire and what you like about them" | No | "None provided" |
| Styles to AVOID | `styles_to_avoid` | String (textarea) | "e.g., cheap effects, overly corporate, meme-style, too slow" | No | "None specified" |
| Narrative structure preference | `narrative_preference` | Options (dropdown) | `Linear story`, `Before/after`, `Problem to solution`, `Montage`, `Interview-based`, `Day-in-the-life`, `Testimonial`, `Abstract/artistic`, `No preference` | No | AI recommends based on content type |

---

### CONSTRAINTS & SPECIFICS (All Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Mandatory elements | `mandatory_elements` | String (textarea) | "Specific shots, logos, taglines, CTA, legal disclaimers, phone numbers, websites that MUST appear" | No | "None" |
| Sensitive considerations | `sensitive_considerations` | String (textarea) | "Cultural sensitivity, legal restrictions, topics to avoid" | No | "None" |
| Quality tier | `quality_tier` | Options (dropdown) | `Premium / cinematic`, `Professional / polished`, `Good / clean`, `Raw / authentic`, `Budget-friendly` | No | "Professional / polished" |
| Subtitles needed? | `subtitles_needed` | Options (dropdown) | `Yes - hardcoded`, `Yes - optional/CC`, `No` | No | AI recommends based on platform |
| Standalone or series? | `series_status` | Options (dropdown) | `Standalone video`, `Part of a series`, `First in a new series` | No | "Standalone video" |
| Series details (if applicable) | `series_details` | String | "Overall series arc or context" | No | "N/A" |

---

## Smart Defaults Reference

When the Brief Builder (Node 02) encounters an empty, blank, or unparsed template variable (e.g., `{{ $form.fieldName }}`), it uses these context-aware inference rules:

| Field | Inference Logic |
|-------|----------------|
| `secondary_platform` | If primary is Instagram Reels → TikTok. If YouTube → Instagram Reels. If TikTok → Instagram Reels. Otherwise → "None". |
| `discovery_method` | If social platform → "Social feed scroll". If YouTube → "Organic search". If Website → "Embedded on website". Otherwise → "Mixed". |
| `sound_assumption` | If TikTok → "Mostly sound ON". If Instagram Reels → "50/50 split". If LinkedIn → "Mostly sound OFF". If YouTube/TV → "Mostly sound ON". |
| `viewer_mindset` | If social short-form → "Passively scrolling". If YouTube → "Actively searching". If corporate → "In a meeting/presentation". |
| `script_status` | Default: "No script yet" |
| `visual_assets` | Default: "Will shoot original footage" |
| `music_status` | Default: "Mood preference only" |
| `music_details` | AI suggests mood/genre based on energy_vibe and content_type |
| `brand_guidelines` | Default: "No brand guidelines" |
| `target_emotions` | AI infers 2-3 emotions from topic, goal, and vibe |
| `energy_vibe` | AI infers from content_type and platform |
| `reference_videos` | Default: "None provided" |
| `styles_to_avoid` | Default: "None specified" |
| `narrative_preference` | AI recommends based on content_type and goal |
| `quality_tier` | Default: "Professional / polished" |
| `subtitles_needed` | If Instagram/LinkedIn/Facebook → "Yes - hardcoded". If YouTube → "Yes - optional/CC". If TV/Cinema → "No". |
| `series_status` | Default: "Standalone video" |
| `series_details` | Default: "N/A" |

---

## Flow State Initialization

In the Start Node's Flow State configuration, initialize:

```json
{
  "project_brief": "",
  "creative_strategy": "",
  "narrative_structure": "",
  "retention_map": "",
  "storyboard": "",
  "pacing_map": "",
  "critique_report": "",
  "critique_grade": "",
  "revision_count": 0,
  "final_package": ""
}
```

---

## Output

The Start Node outputs all form field values, which are accessible in subsequent nodes via:
- `{{ $form.videoTopic }}`
- `{{ $form.contentType }}`
- etc.

Or via flow state references depending on your Flowise version.

