"""The weekly form rule, read from forms.json (the only place the rule is defined)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path=None):
    with open(path or os.path.join(ROOT, "forms.json"), encoding="utf8") as f:
        return json.load(f)


def forms_for(week, cfg=None):
    """Return {"odd": form, "even": form} for a week, or None for a week with no form split."""
    cfg = cfg or load()
    if week in cfg["no_form_weeks"]:
        return None
    a, b = cfg["forms"]
    base_odd = cfg["base_odd"]
    other = b if base_odd == a else a
    flipped = week >= cfg["flip_from_week"] and week % 2 == 1
    odd = other if flipped else base_odd
    even = base_odd if flipped else other
    return {"odd": odd, "even": even}
