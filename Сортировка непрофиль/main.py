import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from src.ui.mode_selector import ModeSelector
from src.infrastructure.services.system_service import SystemService

def main():
    root = tk.Tk()
    root.withdraw()
    
    # Используем выбор файла, чтобы видеть содержимое, но берем только путь к папке
    file_path = filedialog.askopenfilename(
        title="Select ANY file inside the folder you want to organize",
        filetypes=[("All files", "*.*")]
    )
    
    if not file_path:
        # Если файлов в папке нет, откатываемся к обычному выбору папки
        target_dir_str = filedialog.askdirectory(title="Folder is empty or no file selected. Pick folder manually:")
        if not target_dir_str:
            root.destroy()
            return
        target_dir = Path(target_dir_str)
    else:
        target_dir = Path(file_path).parent

    SystemService.open_explorer(target_dir)
    SystemService.open_explorer(target_dir)
    
    selector = ModeSelector(target_dir)
    root.destroy()
    selector.run()

if __name__ == "__main__":
    main()