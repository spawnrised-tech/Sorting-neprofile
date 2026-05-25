import json
from pathlib import Path
from typing import List, Tuple

class HistoryManager:
    HISTORY_FILE = ".sort_history.json"

    def __init__(self, target_dir: Path):
        self.log_path = target_dir / self.HISTORY_FILE

    def save_history(self, moves: List[Tuple[str, str]]):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(moves, f, ensure_ascii=False, indent=4)

    def load_history(self) -> List[Tuple[str, str]]:
        if not self.log_path.exists():
            return []
        with open(self.log_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def clear_history(self):
        if self.log_path.exists():
            self.log_path.unlink()