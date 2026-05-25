from pathlib import Path
from src.domain.contracts.i_sorting_strategy import ISortingStrategy

class SizeStrategy(ISortingStrategy):
    MB = 1024 * 1024
    GB = 1024 * 1024 * 1024

    def get_target_folder(self, file_path: Path) -> str:
        size = file_path.stat().st_size
        if size < 1 * self.MB:
            return "Tiny"
        elif size < 100 * self.MB:
            return "Small"
        elif size < 1 * self.GB:
            return "Medium"
        return "Huge"