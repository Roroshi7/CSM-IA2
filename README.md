## Toll Booth Queue Simulation — Run Instructions

This repository contains a Streamlit dashboard (`app.py`) and a SimPy-based simulator (`simulation.py`) for a toll booth / queue simulation.

The following steps explain how to run this project on a new Windows machine (using PowerShell). They assume you have Python 3.10+ installed.

1) Clone the repository

```powershell
git clone https://github.com/Roroshi7/CSM-IA2.git
cd CSM-IA2
```

2) Create and activate a virtual environment (recommended)

```powershell
python -m venv .venv
# Activate the venv in PowerShell
.\.venv\Scripts\Activate.ps1
# If using cmd.exe instead:
# .\.venv\Scripts\activate.bat
```

3) Install dependencies

There are two possible requirement files included; prefer `requirements.txt` if present, otherwise use `requirements1.txt`.

```powershell
# Preferred (if present)
python -m pip install -r requirements.txt

# Or (fallback)
python -m pip install -r requirements1.txt
```

4) Run the Streamlit app

```powershell
# From inside the activated .venv
python -m streamlit run "app.py"

# Streamlit will print a Local URL (usually http://localhost:8501) — open that in your browser.
```

5) Stopping the app

Press `Ctrl+C` in the PowerShell terminal that is running Streamlit to stop the server.

Notes and troubleshooting
- If `streamlit` isn't found, ensure the venv is activated and you installed the requirements into that environment.
- If you see deprecation warnings about `use_container_width`, those are non-fatal and relate to plotting; the app will still run.
- If you plan to edit or re-run the app frequently, keep the virtual environment activated while working.

Optional: push your changes back to GitHub

```powershell
# Set up repository and push (once configured with your credentials)
git add -A
git commit -m "Add local changes"
git push origin main
```

Contact / Next steps
- If you want, I can: remove compiled `.pyc` files from the repo, add a `.gitignore`, or add more detailed troubleshooting steps.

---
Generated automatically by the workspace tooling to document how to run this project on a new device.
