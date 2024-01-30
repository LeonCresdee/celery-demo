# Fumnail

Demo app for Celery, Flask & Docker

## Commands

### Dev

```bash
docker compose -f ./compose.yml -f ./compose.dev.yml up --force-recreate --build -d
```

### Production

```bash
docker compose up --force-recreate --build -d
```
