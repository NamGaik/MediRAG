"""
results_logger.py  -  one place for every number that goes into the paper.

Put this file in the MediRAG root folder (next to phase_*.py).
In any script, add two lines:

    from results_logger import save_result
    save_result("trajectory", "cv_results", {"hba1c_mae": 0.83, ...})

This writes  results/trajectory/cv_results.json  with a timestamp and the
name of the script that produced it, so every table value is traceable.
"""
import json
import inspect
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(ROOT, "results")


def _to_jsonable(x):
    try:
        import numpy as np
        if isinstance(x, np.generic):
            return x.item()
        if isinstance(x, np.ndarray):
            return x.tolist()
    except ImportError:
        pass
    if isinstance(x, dict):
        return {str(k): _to_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_to_jsonable(v) for v in x]
    return x


def save_result(stage, name, data, notes=""):
    """Save a dict of results to results/<stage>/<name>.json."""
    caller = os.path.basename(inspect.stack()[1].filename)
    folder = os.path.join(RESULTS_DIR, stage)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.json")
    payload = {
        "_produced_by": caller,
        "_saved_at": datetime.now().isoformat(timespec="seconds"),
        "_notes": notes,
        "results": _to_jsonable(data),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"[results] saved -> {os.path.relpath(path, ROOT)}")
    return path