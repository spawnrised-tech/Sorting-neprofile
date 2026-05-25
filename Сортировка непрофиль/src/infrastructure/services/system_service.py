import os
import platform
import subprocess
from pathlib import Path

class SystemService:
    @staticmethod
    def open_explorer(path: Path):
        path_str = str(path.resolve())
        current_os = platform.system()

        if current_os == "Windows":
            os.startfile(path_str)
        elif current_os == "Darwin":
            subprocess.Popen(["open", path_str])
        else:
            subprocess.Popen(["xdg-open", path_str])

    @staticmethod
    def close_explorer(path: Path):
        path_str = str(path.resolve()).rstrip("\\")
        if platform.system() == "Windows":
            cmd = (
                f'$target = "{path_str}".TrimEnd("\\"); '
                f'$shell = New-Object -ComObject Shell.Application; '
                f'$shell.Windows() | Where-Object {{ '
                f'  try {{ $_.Document.Folder.Self.Path.TrimEnd("\\") -ieq $target }} catch {{ $false }} '
                f'}} | ForEach-Object {{ $_.Quit() }}'
            )
            subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", cmd],
                creationflags=0x08000000
            )