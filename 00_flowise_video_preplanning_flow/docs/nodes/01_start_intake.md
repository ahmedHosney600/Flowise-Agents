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
| What is the video about? | `videoTopic` | String (textarea) | "Describe the core topic, subject, product, or message" | **Yes** |
| Primary goal | `primaryGoal` | Options (dropdown) | `Sell a product`, `Educate`, `Entertain`, `Brand awareness`, `Tell a story`, `Document an event`, `Inspire action`, `Go viral`, `Other` | **Yes** |
| Core message (one sentence) | `coreMessage` | String | "The single most important takeaway for the viewer" | **Yes** |
| Content type | `contentType` | Options (dropdown) | `Commercial/Ad`, `YouTube video`, `Short-form Reel/TikTok`, `Corporate/Brand video`, `Documentary`, `Music video`, `Event highlight`, `Product showcase`, `Tutorial`, `Talking head`, `Showreel`, `Short film`, `Real estate`, `Mixed media`, `Motion graphics`, `Other` | **Yes** |
| Target duration | `targetDuration` | Options (dropdown) | `15 seconds`, `30 seconds`, `60 seconds`, `2 minutes`, `3-5 minutes`, `5-10 minutes`, `10+ minutes`, `Flexible` | **Yes** |

---

### AUDIENCE & PLATFORM (Mostly Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Target audience description | `targetAudience` | String (textarea) | "Age range, interests, lifestyle, profession" | **Yes** | — |
| Primary platform | `primaryPlatform` | Options (dropdown) | `YouTube`, `TikTok`, `Instagram Reels`, `Instagram Feed`, `LinkedIn`, `Facebook`, `TV/Broadcast`, `Cinema`, `Website`, `Presentation`, `Other` | **Yes** | — |
| Secondary platform (if any) | `secondaryPlatform` | Options (dropdown) | `None`, `YouTube`, `TikTok`, `Instagram Reels`, `Instagram Feed`, `LinkedIn`, `Facebook`, `TV/Broadcast`, `Website`, `Other` | No | AI infers from primary platform |
| How will viewers discover this? | `discoveryMethod` | Options (dropdown) | `Organic search`, `Paid ads`, `Social feed scroll`, `Direct link`, `Embedded on website`, `TV broadcast`, `Mixed` | No | AI infers from platform |
| Will viewers watch with sound? | `soundAssumption` | Options (dropdown) | `Mostly sound ON`, `Mostly sound OFF`, `50/50 split` | No | AI infers from platform norms |
| Viewer mindset | `viewerMindset` | Options (dropdown) | `Actively searching`, `Passively scrolling`, `In a meeting/presentation`, `At an event`, `Relaxing at home`, `Mixed` | No | AI infers from platform + audience |

---

### ASSETS & RESOURCES (All Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Script / voiceover status | `scriptStatus` | Options (dropdown) | `Full script ready`, `Outline/bullet points`, `No script yet`, `Will improvise`, `Voiceover will be recorded` | No | "No script yet" |
| Visual assets available | `visualAssets` | Options (dropdown) | `Original footage (already filmed)`, `Will shoot original footage`, `Stock footage only`, `Both original + stock`, `Product photos only`, `Screen recordings`, `Graphics/animation`, `None yet` | No | "Will shoot original footage" |
| Music status | `musicStatus` | Options (dropdown) | `Specific track selected`, `Genre preference`, `Mood preference only`, `No preference`, `Will be composed` | No | "Mood preference only" |
| Music details (if any) | `musicDetails` | String | "Genre, mood, or specific track name if selected" | No | AI suggests based on vibe/content type |
| Brand guidelines? | `brandGuidelines` | Options (dropdown) | `Yes - strict guidelines`, `Yes - flexible guidelines`, `No brand guidelines`, `Personal brand` | No | "No brand guidelines" |

---

### CREATIVE DIRECTION (Mostly Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Target emotions (pick up to 3) | `targetEmotions` | String | "e.g., excited, inspired, curious, amazed, amused, empowered" | No | AI infers from topic + goal + vibe |
| Desired energy / vibe | `energyVibe` | Options (dropdown) | `High energy / fast-paced`, `Cinematic / premium`, `Calm / elegant`, `Raw / authentic`, `Playful / fun`, `Dark / moody`, `Corporate / professional`, `Mixed` | No | AI infers from content type + platform |
| Reference videos (if any) | `referenceVideos` | String (textarea) | "Links or descriptions of videos you admire and what you like about them" | No | "None provided" |
| Styles to AVOID | `stylesToAvoid` | String (textarea) | "e.g., cheap effects, overly corporate, meme-style, too slow" | No | "None specified" |
| Narrative structure preference | `narrativePreference` | Options (dropdown) | `Linear story`, `Before/after`, `Problem to solution`, `Montage`, `Interview-based`, `Day-in-the-life`, `Testimonial`, `Abstract/artistic`, `No preference` | No | AI recommends based on content type |

---

### CONSTRAINTS & SPECIFICS (All Optional)

| Field Name | Variable Key | Type | Options / Placeholder | Required | Default if Empty |
|------------|-------------|------|----------------------|----------|-----------------|
| Mandatory elements | `mandatoryElements` | String (textarea) | "Specific shots, logos, taglines, CTA, legal disclaimers, phone numbers, websites that MUST appear" | No | "None" |
| Sensitive considerations | `sensitiveConsiderations` | String (textarea) | "Cultural sensitivity, legal restrictions, topics to avoid" | No | "None" |
| Quality tier | `qualityTier` | Options (dropdown) | `Premium / cinematic`, `Professional / polished`, `Good / clean`, `Raw / authentic`, `Budget-friendly` | No | "Professional / polished" |
| Subtitles needed? | `subtitlesNeeded` | Options (dropdown) | `Yes - hardcoded`, `Yes - optional/CC`, `No` | No | AI recommends based on platform |
| Standalone or series? | `seriesStatus` | Options (dropdown) | `Standalone video`, `Part of a series`, `First in a new series` | No | "Standalone video" |
| Series details (if applicable) | `seriesDetails` | String | "Overall series arc or context" | No | "N/A" |

---

## Smart Defaults Reference

When the Brief Builder (Node 02) encounters an empty, blank, or unparsed template variable (e.g., `{{ $form.fieldName }}`), it uses these context-aware inference rules:

| Field | Inference Logic |
|-------|----------------|
| `secondaryPlatform` | If primary is Instagram Reels → TikTok. If YouTube → Instagram Reels. If TikTok → Instagram Reels. Otherwise → "None". |
| `discoveryMethod` | If social platform → "Social feed scroll". If YouTube → "Organic search". If Website → "Embedded on website". Otherwise → "Mixed". |
| `soundAssumption` | If TikTok → "Mostly sound ON". If Instagram Reels → "50/50 split". If LinkedIn → "Mostly sound OFF". If YouTube/TV → "Mostly sound ON". |
| `viewerMindset` | If social short-form → "Passively scrolling". If YouTube → "Actively searching". If corporate → "In a meeting/presentation". |
| `scriptStatus` | Default: "No script yet" |
| `visualAssets` | Default: "Will shoot original footage" |
| `musicStatus` | Default: "Mood preference only" |
| `musicDetails` | AI suggests mood/genre based on energyVibe and contentType |
| `brandGuidelines` | Default: "No brand guidelines" |
| `targetEmotions` | AI infers 2-3 emotions from topic, goal, and vibe |
| `energyVibe` | AI infers from contentType and platform |
| `referenceVideos` | Default: "None provided" |
| `stylesToAvoid` | Default: "None specified" |
| `narrativePreference` | AI recommends based on contentType and goal |
| `qualityTier` | Default: "Professional / polished" |
| `subtitlesNeeded` | If Instagram/LinkedIn/Facebook → "Yes - hardcoded". If YouTube → "Yes - optional/CC". If TV/Cinema → "No". |
| `seriesStatus` | Default: "Standalone video" |
| `seriesDetails` | Default: "N/A" |

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

