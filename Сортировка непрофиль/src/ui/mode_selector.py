import tkinter as tk
from tkinter import filedialog, messagebox
from src.infrastructure.services.system_service import SystemService
from src.infrastructure.services.file_organizer import FileOrganizer
from src.domain.strategies.type_strategy import TypeStrategy
from src.domain.strategies.date_strategy import DateStrategy
from src.domain.strategies.size_strategy import SizeStrategy
from src.domain.strategies.name_strategy import NameStrategy

from tkinter import ttk

class ModeSelector:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self._root = tk.Tk()
        self._root.title("Smart File Organizer")
        self._root.geometry("450x500")
        self._root.configure(bg="#f5f5f5")
        
        self._style = ttk.Style()
        self._style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self._style.configure("Action.TButton", foreground="#2196F3")
        self._style.configure("Undo.TButton", foreground="#f44336")
        
        self._setup_ui()

    def _setup_ui(self):
        # --- Header Section ---
        header_frame = tk.Frame(self._root, bg="#ffffff", height=80, bd=1, relief=tk.FLAT)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame, text="Active Directory", 
            font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#888888"
        ).pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.path_label = tk.Label(
            header_frame, text=str(self.target_dir), 
            font=("Segoe UI", 10), bg="#ffffff", fg="#333333", 
            wraplength=400, justify=tk.LEFT
        )
        self.path_label.pack(anchor=tk.W, padx=20, pady=(0, 10))

        # --- Content Section ---
        body_frame = tk.Frame(self._root, bg="#f5f5f5")
        body_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(
            body_frame, text="How should I sort your files?", 
            font=("Segoe UI", 11), bg="#f5f5f5", fg="#444444"
        ).grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Растягиваем колонку на всю ширину
        body_frame.columnconfigure(0, weight=1)

        modes = [
            ("📁 By File Type", "Sorts by extension (Images, Documents, Videos...)", TypeStrategy()),
            ("📅 By Modification Date", "Groups files into folders by Year-Month", DateStrategy()),
            ("⚖️ By File Size", "Categorizes as Tiny, Small, Medium, or Huge", SizeStrategy()),
            ("🔤 By First Letter", "Organizes into folders based on name initials", NameStrategy())
        ]

        for i, (name, desc, strategy) in enumerate(modes):
            btn_frame = tk.LabelFrame(body_frame, text="", bg="#ffffff", bd=1, relief=tk.FLAT)
            btn_frame.grid(row=i+1, column=0, pady=4, sticky="ew")
            
            # Внутренняя компоновка карточки: кнопка слева, описание справа
            ttk.Button(
                btn_frame, text=name, 
                command=lambda s=strategy: self._on_exec(s),
                width=25
            ).pack(side=tk.LEFT, padx=15, pady=12)
            
            tk.Label(
                btn_frame, text=desc, font=("Segoe UI", 8), 
                bg="#ffffff", fg="#888888", justify=tk.LEFT
            ).pack(side=tk.LEFT, padx=(0, 15), fill=tk.X)

        # --- Footer Section ---
        footer_frame = tk.Frame(self._root, bg="#f5f5f5")
        footer_frame.pack(fill=tk.X, padx=20, pady=20)

        self.btn_change = ttk.Button(
            footer_frame, text="🔄 Change Directory", 
            command=self._on_change_dir, style="Action.TButton"
        )
        self.btn_change.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.btn_undo = ttk.Button(
            footer_frame, text="↩️ Undo Last", 
            command=self._on_undo, style="Undo.TButton"
        )
        self.btn_undo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready to organize")
        status_bar = tk.Label(
            self._root, textvariable=self.status_var, 
            bd=1, relief=tk.SUNKEN, anchor=tk.W, 
            font=("Segoe UI", 8), bg="#eeeeee"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_exec(self, strategy):
        organizer = FileOrganizer(strategy)
        self.status_var.set(f"Sorting by {strategy.__class__.__name__}...")
        self._root.update_idletasks()
        try:
            organizer.run(self.target_dir)
            self.status_var.set("Sorting complete!")
            messagebox.showinfo("Success", "Files organized successfully.")
        except Exception as e:
            self.status_var.set("Error occurred.")
            messagebox.showerror("Error", str(e))

    def _on_undo(self):
        organizer = FileOrganizer(None)
        try:
            organizer.undo(self.target_dir)
            messagebox.showinfo("Success", "Undo complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_change_dir(self):
        # Используем тот же визуальный метод при смене директории
        file_path = filedialog.askopenfilename(
            title="Select any file in the new folder",
            filetypes=[("All files", "*.*")]
        )
        
        if file_path:
            new_dir = Path(file_path).parent
        else:
            # Если пользователь не выбрал файл (например, папка пуста), даем выбрать папку
            new_dir_str = filedialog.askdirectory(title="Or select folder directly:")
            if not new_dir_str:
                return
            new_dir = Path(new_dir_str)

        SystemService.close_explorer(self.target_dir)
        self.target_dir = new_dir
        self._root.title(f"Organizer: {self.target_dir.name}")
        self.path_label.config(text=str(self.target_dir))
        self._root.update()
        SystemService.open_explorer(self.target_dir)

    def run(self):
        self._root.mainloop()