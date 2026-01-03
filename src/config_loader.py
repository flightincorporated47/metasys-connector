# config_loader.py
import os
import re
import yaml
from typing import Any, Dict

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")

def _expand_env(value: Any) -> Any:
    if isinstance(value, str):
        def repl(m):
            key = m.group(1)
            return os.environ.get(key, "")
        return _ENV_PATTERN.sub(repl, value)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(v) for v in value]
    return value

def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return _expand_env(raw)
