from abc import ABC, abstractmethod
from pathlib import Path

class IFileOrganizer(ABC):
    """Contract for file organization services."""
    
    @abstractmethod
    def organize(self, target_path: Path) -> None:
        """
        Organizes files in the given directory by their extensions.
        @param target_path: The directory to clean up.
        """
        pass