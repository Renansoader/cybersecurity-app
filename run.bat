@echo off
REM Abre o app. Usa a .venv da pasta se ela existir; senao, o Python do sistema.
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else (
    start "" pythonw main.py
)
