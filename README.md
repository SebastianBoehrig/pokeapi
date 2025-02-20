# Pokeapi

## Description

a small app to show pokemon from pokeapi

## Settup + Run Dev

Windows:

```powershell
cd .\backend
python -m venv .venv
.venv\Scripts\Activate
pip install -r .\requirements-dev.txt
```

```powershell
fastapi run .\app\main.py --host 127.0.0.1 --port 8080 --reload
```

Other:

```bash
cd ./backend
python -m venv .venv
source .venv/bin/activate
pip install -r ./requirements-dev.txt
```

```bash
fastapi run ./app/main.py --host 127.0.0.1 --port 8080 --reload
```

## Run Tests

Windows:

```powershell
cd .\backend
pytest
mypy .\app
```

Other:

```bash
cd ./backend
pytest
mypy ./app
```
