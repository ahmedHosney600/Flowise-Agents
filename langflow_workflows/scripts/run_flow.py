"""
Direct Execution Script for Converted Video Pipelines
Runs any of the 3 video storytelling flows directly against the gemini-web-to-api proxy.
"""

import json
import os
import sys
import re
from openai import OpenAI

# Connect to running local Gemini proxy
PROXY_BASE_URL = "http://localhost:4981/openai/v1"
client = OpenAI(base_url=PROXY_BASE_URL, api_key="not-needed")

def call_llm(system_prompt: str, user_prompt: str, model="gemini-2.0-flash", temp=0.7) -> str:
    print("  ⚡ Sending request to Gemini...", end="", flush=True)
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temp
        )
        out = res.choices[0].message.content
        print(" Done!")
        return out
    except Exception as e:
        print(f"\n❌ LLM Call Failed: {e}")
        return f"Error: {e}"

def extract_grade(critique_text: str) -> str:
    # Try JSON extraction
    try:
        fenced = re.search(r"```json\s*([\s\S]*?)```", critique_text, re.IGNORECASE)
        json_str = fenced.group(1) if fenced else None
        if not json_str:
            json_match = re.search(r"\{[\s\S]*\}", critique_text)
            json_str = json_match.group(0) if json_match else None
        if json_str:
            data = json.loads(json_str)
            if "critique_grade" in data:
                clean = re.sub(r"[^A-Za-z+]", "", str(data["critique_grade"])).strip().upper()
                if clean in ["A+", "A", "B", "C", "D"]:
                    return clean
    except Exception:
        pass

    # Regex fallback
    match = re.search(r"(?:Overall Grade|FINAL_GRADE|Post-Revision Grade)[\s\S]*?[:\*]*\s*\[?([A-Da-d]\+?)", critique_text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "C"

def run_speed_ramp_pipeline():
    print("\n" + "=" * 60)
    print("🎬 RUNNING: 02 Speed Ramp & Viral Edit Pipeline")
    print("=" * 60)

    flow = json.load(open("flows/02_speed_ramp_viral_flow.json"))
    nodes = {n["id"]: n for n in flow["data"]["nodes"]}

    state = {
        "preplanning_package": "Supercar acceleration & drift speed-ramp montage (9:16 Vertical)",
        "clip_descriptions": "Clip 1: Driver helmet close-up (4s)\nClip 2: Exhaust flames rev (3s)\nClip 3: Hard launch wheelspin (5s)\nClip 4: High-speed drift apex (6s)\nClip 5: FPV drone chase spoiler (4s)\nClip 6: Slide to stop driver stare down (4s)",
        "target_duration": "30 seconds",
        "music_bpm": "135",
        "music_drops": "0:02.80, 0:08.50, 0:15.20, 0:22.40",
        "source_framerate": "60fps / 120fps",
        "revision_count": "0",
        "revised_plans": ""
    }

    # Step 1: Clip Arrangement
    print("\n[Step 1/6] 📋 Designing Clip Arrangement...")
    node1 = nodes["agent_01_arrangement"]["data"]["node"]["template"]
    sys_p = node1["system_prompt"]["value"]
    usr_p = f"PRE-PLANNING PACKAGE:\n{state['preplanning_package']}\n\nCLIP DESCRIPTIONS:\n{state['clip_descriptions']}\n\nTARGET DURATION: {state['target_duration']}\nMUSIC BPM: {state['music_bpm']}\nMUSIC DROP TIMESTAMPS: {state['music_drops']}\nSOURCE FRAME RATE: {state['source_framerate']}"
    state["clip_arrangement"] = call_llm(sys_p, usr_p)

    # Step 2: Speed Ramp Designer
    print("\n[Step 2/6] ⚡ Designing Speed Ramp Keyframes & Curves...")
    node2 = nodes["agent_02_speed_ramp"]["data"]["node"]["template"]
    sys_p = node2["system_prompt"]["value"]
    usr_p = f"CLIP ARRANGEMENT:\n{state['clip_arrangement']}\n\nMUSIC BPM: {state['music_bpm']}\nMUSIC DROP TIMESTAMPS: {state['music_drops']}\nSOURCE FRAME RATE: {state['source_framerate']}"
    state["speed_ramp_plan"] = call_llm(sys_p, usr_p)

    # Step 3: Viral Effects
    print("\n[Step 3/6] ✨ Designing Viral Effects & Transitions...")
    node3 = nodes["agent_03_effects"]["data"]["node"]["template"]
    sys_p = node3["system_prompt"]["value"]
    usr_p = f"CLIP ARRANGEMENT:\n{state['clip_arrangement']}\n\nSPEED RAMP PLAN:\n{state['speed_ramp_plan']}"
    state["viral_effects_plan"] = call_llm(sys_p, usr_p)

    # Step 4: Sound Design
    print("\n[Step 4/6] 🔊 Creating Sound Design & Sourcing Shopping List...")
    node4 = nodes["agent_04_sound"]["data"]["node"]["template"]
    sys_p = node4["system_prompt"]["value"]
    usr_p = f"CLIP ARRANGEMENT:\n{state['clip_arrangement']}\n\nSPEED RAMP PLAN:\n{state['speed_ramp_plan']}\n\nVIRAL EFFECTS PLAN:\n{state['viral_effects_plan']}\n\nMUSIC BPM: {state['music_bpm']}"
    state["sound_finishing_plan"] = call_llm(sys_p, usr_p)

    # Step 5: Self-Critique Audit
    print("\n[Step 5/6] 🧐 Auditing Pipeline & Viral Quality...")
    node5 = nodes["agent_05_critique"]["data"]["node"]["template"]
    sys_p = node5["system_prompt"]["value"]
    usr_p = f"CLIP ARRANGEMENT:\n{state['clip_arrangement']}\n\nSPEED RAMP PLAN:\n{state['speed_ramp_plan']}\n\nVIRAL EFFECTS PLAN:\n{state['viral_effects_plan']}\n\nSOUND & FINISHING PLAN:\n{state['sound_finishing_plan']}\n\nMUSIC BPM: {state['music_bpm']}"
    critique_res = call_llm(sys_p, usr_p)
    grade = extract_grade(critique_res)
    print(f"  ⭐ Audit Letter Grade Assigned: {grade}")

    # Step 6: Final Viral Package
    print("\n[Step 6/6] 📦 Compiling Master Final Viral Package...")
    node6 = nodes["agent_06_package"]["data"]["node"]["template"]
    sys_p = node6["system_prompt"]["value"]
    usr_p = f"CLIP ARRANGEMENT:\n{state['clip_arrangement']}\n\nSPEED RAMP PLAN:\n{state['speed_ramp_plan']}\n\nVIRAL EFFECTS PLAN:\n{state['viral_effects_plan']}\n\nSOUND & FINISHING PLAN:\n{state['sound_finishing_plan']}\n\nCRITIQUE REPORT:\n{critique_res}\n\nCLIP COUNT: 6 clips"
    final_package = call_llm(sys_p, usr_p)

    # Save deliverable
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/speed_ramp_viral_package.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_package)

    print("\n" + "=" * 60)
    print(f"🎉 SUCCESS! Final deliverable saved to: {out_path}")
    print("=" * 60)

if __name__ == "__main__":
    run_speed_ramp_pipeline()
