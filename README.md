# Fumnail

Demo app for Celery, Flask & Docker

## Commands

### Dev

```bash
docker compose -f ./compose.yml -f ./compose.dev.yml up -d
```

### Production

```bash
docker compose build --no-cache
docker compose up -d
```
