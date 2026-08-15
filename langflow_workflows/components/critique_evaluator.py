"""
Langflow Custom Component: Critique Evaluator & Loop Guard
Deterministic grading and revision loop handling for video storytelling pipelines.
"""

from typing import Dict, Any
import re
import json

try:
    from langflow.custom import Component
    from langflow.io import MessageTextInput, Output, IntInput, DropdownInput
    from langflow.schema import Message
except ImportError:
    # Fallback / standalone mode
    class Component:
        pass
    def MessageTextInput(**kwargs): return kwargs
    def Output(**kwargs): return kwargs
    def IntInput(**kwargs): return kwargs
    def DropdownInput(**kwargs): return kwargs
    class Message:
        def __init__(self, text=""): self.text = text


class CritiqueEvaluator(Component):
    display_name = "Critique Evaluator & Loop Guard"
    description = "Parses Self-Critique audit, extracts grade (A+, A, B, C, D), and deterministically guards revision loops."
    icon = "check-circle"
    name = "CritiqueEvaluator"

    inputs = [
        MessageTextInput(
            name="critique_output",
            display_name="Critique Output",
            info="The raw text or JSON string from the Self-Critique LLM node.",
        ),
        IntInput(
            name="current_revision_count",
            display_name="Current Revision Count",
            value=0,
            info="Current iteration count (0 = initial pass, 1 = pass 1, etc.)",
        ),
        IntInput(
            name="max_loops",
            display_name="Max Allowed Loops",
            value=2,
            info="Maximum revision passes before forcing final deliverable generation.",
        ),
    ]

    outputs = [
        Output(display_name="Grade", name="grade", method="get_grade"),
        Output(display_name="Status", name="status", method="get_status"),
        Output(display_name="Next Revision Count", name="next_revision_count", method="get_next_count"),
        Output(display_name="Revision Fixes", name="revision_fixes", method="get_fixes"),
        Output(display_name="Clean Audit Report", name="clean_report", method="get_report"),
    ]

    def _parse_audit(self) -> Dict[str, Any]:
        raw = str(getattr(self, "critique_output", "") or "").strip()
        grade = "C"
        report = raw
        fixes = ""

        # 1. Try parsing JSON (fenced or unfenced)
        try:
            fenced = re.search(r"```json\s*([\s\S]*?)```", raw, re.IGNORECASE)
            json_str = fenced.group(1) if fenced else None
            if not json_str:
                json_match = re.search(r"\{[\s\S]*\}", raw)
                json_str = json_match.group(0) if json_match else None

            if json_str:
                data = json.loads(json_str)
                if isinstance(data, dict):
                    if "critique_grade" in data:
                        clean = re.sub(r"[^A-Za-z+]", "", str(data["critique_grade"])).strip().upper()
                        if clean in ["A+", "A", "B", "C", "D"]:
                            grade = clean
                    if "critique_report" in data and str(data["critique_report"]).strip():
                        report = str(data["critique_report"])
                    if "revised_plans" in data:
                        fixes = str(data["revised_plans"])
                    elif "revised_storyboard" in data:
                        fixes = str(data["revised_storyboard"])
        except Exception:
            pass

        # 2. Regex fallback for grade
        if grade == "C":
            grade_match = re.search(r"(?:Overall Grade|FINAL_GRADE|Post-Revision Grade)[\s\S]*?[:\*]*\s*\[?([A-Da-d]\+?)", raw, re.IGNORECASE)
            if grade_match:
                extracted = grade_match.group(1).upper()
                if extracted in ["A+", "A", "B", "C", "D"]:
                    grade = extracted

        # Determine loop & approval status
        current_count = int(getattr(self, "current_revision_count", 0) or 0)
        max_loops = int(getattr(self, "max_loops", 2) or 2)

        is_grade_approved = "A" in grade  # A+ or A
        is_max_loops_reached = current_count >= max_loops

        if is_grade_approved:
            status = "APPROVED"
        elif is_max_loops_reached:
            status = "MAX_LOOPS_REACHED"
        else:
            status = "NEEDS_REVISION"

        return {
            "grade": grade,
            "status": status,
            "next_revision_count": current_count + 1,
            "revision_fixes": fixes if fixes else report,
            "clean_report": report,
        }

    def get_grade(self) -> Message:
        parsed = self._parse_audit()
        return Message(text=parsed["grade"])

    def get_status(self) -> Message:
        parsed = self._parse_audit()
        return Message(text=parsed["status"])

    def get_next_count(self) -> Message:
        parsed = self._parse_audit()
        return Message(text=str(parsed["next_revision_count"]))

    def get_fixes(self) -> Message:
        parsed = self._parse_audit()
        return Message(text=parsed["revision_fixes"])

    def get_report(self) -> Message:
        parsed = self._parse_audit()
        return Message(text=parsed["clean_report"])
