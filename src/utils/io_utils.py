import json
from datetime import datetime
from pathlib import Path


def save_metrics(metrics: dict, metrics_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = metrics_dir / f"run_metrics_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    return output_file