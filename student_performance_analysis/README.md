# Student Performance Analysis System

A beginner-friendly Flask + SQLite mini project.

## Features
- Dashboard with total students, average marks, attendance, and students needing support
- Add student records
- Subject-wise performance averages
- Automatic average and grade classification
- Delete student records
- SQLite database created automatically
- Sample data added on first run

## Requirements
- Python 3.10 or newer recommended
- Visual Studio Code
- Python extension for VS Code

## Run in VS Code

1. Extract this ZIP file.
2. Open the extracted `student_performance_analysis` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   Windows:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If `py` is not recognized, try `python -m venv .venv`.
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install Flask:
   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the app:
   ```bash
   python app.py
   ```

7. Open the address printed in the terminal, usually:
   `http://127.0.0.1:5000`

Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop it.

## Notes
- Sample students are included for demonstration; remove them before using real records.
- This is a learning prototype, not a production-ready system. Add authentication, authorization, secure configuration, and backups before using real student data.
- Grade bands are examples and should be adjusted to your institution's rules.
