#!/bin/bash

# --- CONFIGURARE ---
DB_NAME="art_nouveau"
DB_USER="floron"
DB_HOST="localhost"
DB_PORT="5432"
OUTPUT_FILE="backup_data.sql"

echo "=== Începere proces Backup pentru $DB_NAME ==="

# Explicatie flag-uri:
# --column-inserts     -> Generează comenzi INSERT INTO table (col1, col2) VALUES ...
# --data-only          -> Nu exportă CREATE TABLE (structura o faci tu prin migrări)
# --exclude-table-data -> Excludem tabelul de istoric al migrarilor pentru a nu intra in conflict
#                         când rulezi 'python manage.py migrate' pe o bază curată.

pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER \
    --column-inserts \
    --data-only \
    --exclude-table-data 'django_migrations' \
    --exclude-table-data 'django_content_type' \
    $DB_NAME > $OUTPUT_FILE

if [ $? -eq 0 ]; then
    echo "Succes! Fisierul '$OUTPUT_FILE' a fost generat."
    echo "Conține comenzi INSERT pentru datele tale."
else
    echo "Eroare la generarea backup-ului."
fi

unset PGPASSWORD