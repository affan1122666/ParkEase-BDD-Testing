# ParkEase BDD Automation

## Requirements
- Python 3.10 or newer
- pip

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Run all scenarios
From the project root, run this single command:

```bash
python -m behave
```

The console output is shown and an HTML report is written to `reports/report.html`.

## Run selected groups
```bash
python -m behave --tags=@smoke
python -m behave --tags=@boundary
python -m behave --tags=@negative
```

The model is intentionally in-memory; it does not require a database or a real mobile app.
