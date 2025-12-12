import json
import re
from datetime import datetime
from typing import Optional, Any


def timestamped_log(message: str) -> str:
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] {message}"
    print(entry)
    return entry


def safe_extract_json(text: str) -> Optional[Any]:
    """Try to extract the first JSON array or object from `text` and parse it.

    Returns the parsed object or None if parsing fails.
    """
    if not text:
        return None
    # Try to find a JSON array first
    patterns = [r"(\[\s*\{.*?\}\s*\])", r"(\{.*?\})"]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL)
        if m:
            candidate = m.group(1)
            try:
                return json.loads(candidate)
            except Exception:
                continue
    # Last resort: try to load the whole text
    try:
        return json.loads(text)
    except Exception:
        return None


__all__ = ["timestamped_log", "safe_extract_json"]
