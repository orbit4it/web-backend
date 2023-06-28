# Orbit Web Backend

Backend GraphQL API untuk web Orbit.

## Menjalankan server

1. Clone repository ini
2. buat .env file ([Lihat contoh](https://github.com/orbit4it/web-backend/blob/main/.env.example))
3. Install dependensi & jalankan server:

```
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Mengelola database

Skema database akan dibuat secara otomatis saat server dijalankan. Jika ada perubahan skema, maka tabel harus didrop terlebih dahulu. Untuk melakukan drop table dan seeder gunakan `script.py`

Drop semua table:

```
python script.py drop-all

```

Seeder (create data dummy):

```
python script.py seed

```
