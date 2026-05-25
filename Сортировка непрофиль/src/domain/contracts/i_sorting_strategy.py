from abc import ABC, abstractmethod
from pathlib import Path

class ISortingStrategy(ABC):
    @abstractmethod
    def get_target_folder(self, file_path: Path) -> str:
        pass