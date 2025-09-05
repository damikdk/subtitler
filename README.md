# Subtitler

## Deploy with docker

```bash
git clone https://github.com/damikdk/subtitler.git
cd subtitler
echo "API_KEY=your-secret-key-change-this-in-production" > .env
docker compose up --build -d
```

## Deploy with command
```bash
nohup uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 > api.log 2>&1 &
```

## Just run
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```
