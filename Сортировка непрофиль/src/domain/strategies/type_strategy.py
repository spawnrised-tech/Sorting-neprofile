from pathlib import Path
from src.domain.contracts.i_sorting_strategy import ISortingStrategy

class TypeStrategy(ISortingStrategy):
    MAP = {
        "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"},
        "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"},
        "Videos": {".mp4", ".mov", ".avi", ".mkv"},
        "Audio": {".mp3", ".wav", ".flac"},
        "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    }

    def get_target_folder(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()
        for category, extensions in self.MAP.items():
            if extension in extensions:
                return category
        return "Others"