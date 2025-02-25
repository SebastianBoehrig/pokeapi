# Pokeapi

## Description

a small app to show pokemon from pokeapi

## Settup + Run Prod

```bash
docker compose up --build
```

the go to `http://localhost:8080`

## Backend Settup + Run Dev

Windows:

```powershell
cd .\backend
python -m venv .venv
.venv\Scripts\Activate
pip install -r .\requirements-dev.txt
```

```powershell
fastapi run .\app\main.py --host 127.0.0.1 --port 8181 --reload
```

Other:

```bash
cd ./backend
python -m venv .venv
source .venv/bin/activate
pip install -r ./requirements-dev.txt
```

```bash
fastapi run ./app/main.py --host 127.0.0.1 --port 8181 --reload
```

## Run Tests

Windows:

```powershell
cd .\backend
pytest
pyright .\app\
```

Other:

```bash
cd ./backend
pytest
pyright ./app
```

## Frontend Settup + Run Dev

Windows:

```powershell
cd .\frontend
npm install
```

```powershell
npm run dev
```

Other:

```bash
cd ./frontend
npm install
```

```bash
npm run dev
```
