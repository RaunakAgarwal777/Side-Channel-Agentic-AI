"""
results.py
Persists benchmark/evaluation output to disk (JSON + CSV) so results can
be tracked across runs and pulled into the paper's results section.
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, Any


class ResultsWriter:
    def __init__(self, output_dir: str = "./results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write(self, report: Dict[str, Any]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(self.output_dir, f"run_{timestamp}.json")
        with open(json_path, "w") as f:
            json.dump(report, f, indent=2, default=str)

        csv_path = os.path.join(self.output_dir, "runs_summary.csv")
        flat = self._flatten(report)
        flat["timestamp"] = timestamp
        file_exists = os.path.isfile(csv_path)
        with open(csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(flat)

        return json_path

    @staticmethod
    def _flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        flat = {}
        for k, v in d.items():
            key = f"{prefix}{k}"
            if isinstance(v, dict):
                flat.update(ResultsWriter._flatten(v, prefix=f"{key}_"))
            else:
                flat[key] = v
        return flat
