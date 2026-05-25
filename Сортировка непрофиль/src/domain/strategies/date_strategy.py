import datetime
from pathlib import Path
from src.domain.contracts.i_sorting_strategy import ISortingStrategy

class DateStrategy(ISortingStrategy):
    def get_target_folder(self, file_path: Path) -> str:
        timestamp = file_path.stat().st_mtime
        date = datetime.datetime.fromtimestamp(timestamp)
        return date.strftime("%Y-%m")