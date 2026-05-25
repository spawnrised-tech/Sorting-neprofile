from pathlib import Path
from src.domain.contracts.i_sorting_strategy import ISortingStrategy

class NameStrategy(ISortingStrategy):
    def get_target_folder(self, file_path: Path) -> str:
        first_char = file_path.name[0].upper()
        if first_char.isalpha():
            return first_char
        return "Symbols"