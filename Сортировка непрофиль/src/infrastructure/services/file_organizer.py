import shutil
from pathlib import Path
from src.domain.contracts.i_sorting_strategy import ISortingStrategy
from src.infrastructure.services.history_manager import HistoryManager

class FileOrganizer:
    def __init__(self, strategy: ISortingStrategy):
        self.strategy = strategy

    def run(self, directory: Path):
        history = HistoryManager(directory)
        moves = []

        for item in directory.iterdir():
            if self._should_skip(item):
                continue
            
            folder_name = self.strategy.get_target_folder(item)
            target_dir = directory / folder_name
            target_dir.mkdir(exist_ok=True)
            
            final_path = self._move_safely(item, target_dir)
            moves.append((str(final_path), str(item)))
        
        history.save_history(moves)

    def undo(self, directory: Path):
        history_manager = HistoryManager(directory)
        moves = history_manager.load_history()

        for current, original in moves:
            curr_path = Path(current)
            orig_path = Path(original)
            
            if curr_path.exists():
                shutil.move(str(curr_path), str(orig_path))
                parent_dir = curr_path.parent
                if parent_dir != directory and not any(parent_dir.iterdir()):
                    parent_dir.rmdir()

        history_manager.clear_history()

    def _should_skip(self, item: Path) -> bool:
        if item.is_dir() or item.name.startswith('.'):
            return True
        program_files = {'main.py', 'src', 'SmartOrganizer.exe'}
        return item.name in program_files or item.suffix == ".py"

    def _move_safely(self, file: Path, target_dir: Path) -> Path:
        destination = target_dir / file.name
        if destination.exists():
            counter = 1
            while True:
                candidate = target_dir / f"{file.stem}_{counter}{file.suffix}"
                if not candidate.exists():
                    destination = candidate
                    break
                counter += 1
        shutil.move(str(file), str(destination))
        return destination