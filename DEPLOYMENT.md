# Deployment Guide

## Docker

```bash
# Build
docker build -t task_master .

# Run
docker run -d -p 8000:8000 --name task_master task_master

# Logs
docker logs task_master
```

## Railway

1. Push to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Set `PORT=8000` environment variable
4. Railway auto-detects the Dockerfile

## Render

1. Push to GitHub
2. Create new **Web Service** on [Render](https://render.com)
3. Build command: `pip install -r app/requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT signing secret | Yes |
| `DATABASE_URL` | SQLAlchemy DB URL (default: SQLite) | No |
| `PORT` | Server port (default: 8000) | No |

## Production Checklist

- [ ] Set `SECRET_KEY` to a random 32+ char string
- [ ] Use PostgreSQL instead of SQLite for production
- [ ] Enable HTTPS (handled by Railway/Render automatically)
- [ ] Set `CORS_ORIGINS` to your frontend domain
