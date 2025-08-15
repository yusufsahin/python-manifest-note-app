# manifest-api (0.1.0)

Manifest (JSON) ile dinamik CRUD FastAPI sunucusu. Kod yazmadan yeni varlık ekleyin.

## Kurulum
```bash
# İnternete bağlı bir ortamda, bu zip'i indirdikten sonra:
pip install manifest-api-0.1.0.zip

# veya klasöre çıkarıp:
pip install .
```

## Kullanım
```bash
# Basit başlatma (varsayılan SQLite ./manifest.db)
manifest-api --manifest ./example/manifest.json --host 127.0.0.1 --port 8000 --reload

# PostgreSQL ile (opsiyonel)
export DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/manifestdb
manifest-api --manifest ./example/manifest.json
```
- Docs: http://127.0.0.1:8000/docs
- Health: /health
