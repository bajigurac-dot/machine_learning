#!/bin/bash
# ==============================================================================
# Script Backup Database SQLite (Nilai Siswa & Soal Ujian)
# ==============================================================================

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TARGET_FILE="${BACKUP_DIR}/studio_ml_backup_${TIMESTAMP}.db"

mkdir -p "$BACKUP_DIR"

if [ -f "data/studio_ml.db" ]; then
    cp "data/studio_ml.db" "$TARGET_FILE"
    echo "✅ Backup berhasil dibuat: $TARGET_FILE"
elif [ -f "studio_ml.db" ]; then
    cp "studio_ml.db" "$TARGET_FILE"
    echo "✅ Backup berhasil dibuat: $TARGET_FILE"
else
    echo "❌ Error: File database tidak ditemukan!"
    exit 1
fi
