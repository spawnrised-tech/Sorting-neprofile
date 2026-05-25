@echo off
echo Starting build process...
pyinstaller --noconsole --onefile --name "SmartOrganizer" --add-data "src;src" main.py
echo Build finished! Check the 'dist' folder.
pause