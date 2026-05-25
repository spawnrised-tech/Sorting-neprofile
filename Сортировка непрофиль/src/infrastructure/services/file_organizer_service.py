import shutil
from pathlib import Path
from src.domain.contracts.i_file_organizer import IFileOrganizer
from src.domain.models.file_categories import FileCategories

class FileOrganizerService(IFileOrganizer):
    def organize(self, target_path: Path) -> None:
        if not target_path.exists() or not target_path.is_dir():
            return

        for item in target_path.iterdir():
            if self._should_skip(item):
                continue
            
            category = self._get_category(item.suffix.lower())
            destination_dir = target_path / category
            
            self._ensure_directory_exists(destination_dir)
            self._move_file(item, destination_dir)

    def _should_skip(self, item: Path) -> bool:
        return item.is_dir() or item.name.startswith('.') or item.name == "main.py"

    def _get_category(self, extension: str) -> str:
        for category, extensions in FileCategories.MAP.items():
            if extension in extensions:
                return category
        return FileCategories.DEFAULT_FOLDER

    def _ensure_directory_exists(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)

    def _move_file(self, source: Path, destination_dir: Path) -> None:
        target_path = destination_dir / source.name
        
        if target_path.exists():
            target_path = self._resolve_collision(destination_dir, source)
            
        shutil.move(str(source), str(target_path))

    def _resolve_collision(self, destination_dir: Path, source: Path) -> Path:
        counter = 1
        while True:
            new_name = f"{source.stem}_{counter}{source.suffix}"
            new_path = destination_dir / new_name
            if not new_path.exists():
                return new_path
            counter += 1