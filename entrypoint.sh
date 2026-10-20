#!/bin/sh
set -e

echo "==> [Entrypoint] Starting Konkan Guide container..."

# 1. Wait for database if PostgreSQL is used
if [ -n "$DATABASE_URL" ]; then
    echo "==> [Entrypoint] Checking database availability..."
    python << 'EOF'
import os
import sys
import time
import dj_database_url
import psycopg2

db_url = os.environ.get('DATABASE_URL', '')
if 'postgres' in db_url:
    config = dj_database_url.parse(db_url)
    user = config.get('USER')
    password = config.get('PASSWORD')
    host = config.get('HOST', 'localhost')
    port = config.get('PORT', 5432)
    dbname = config.get('NAME')

    max_retries = 30
    retry = 0
    while retry < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                connect_timeout=3
            )
            conn.close()
            print(f"==> [Entrypoint] Successfully connected to database at {host}:{port}!")
            sys.exit(0)
        except Exception as e:
            retry += 1
            print(f"==> [Entrypoint] Waiting for database at {host}:{port}... (attempt {retry}/{max_retries})")
            time.sleep(2)
    print("==> [Entrypoint] WARNING: Could not verify direct connection to database. Proceeding anyway.")
EOF
fi

# 2. Run database migrations safely
if [ "$RUN_MIGRATIONS" != "False" ]; then
    echo "==> [Entrypoint] Applying database migrations..."
    python manage.py migrate --noinput
fi

# 3. Collect static files
if [ "$COLLECT_STATIC" != "False" ]; then
    echo "==> [Entrypoint] Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

# 4. Optional Initial Data Seeding
if [ "$AUTO_SEED_DATA" = "True" ]; then
    echo "==> [Entrypoint] Seeding companion and operations data..."
    python manage.py seed_companion_data || true
fi

echo "==> [Entrypoint] Initialization complete. Executing command: $@"
exec "$@"
