#!/bin/bash
# ==============================================================================
# Script Update Kode & Database Baru di AWS EC2
# ==============================================================================

set -e

echo "========================================================="
echo "🔄 Memulai Proses Update Studio ML & E-Learning di EC2..."
echo "========================================================="

# 1. Tarik pembaruan kode dan file database terbaru dari GitHub
echo "📥 Menarik commit terbaru dari branch main..."
git fetch origin main
# Buang perubahan lokal sementara di EC2 agar pull tidak pernah bentrok/conflict
git checkout -- studio_ml.db 2>/dev/null || true
git reset --hard origin/main

# 2. Backup database yang saat ini sedang aktif di EC2
echo "💾 Membuat salinan cadangan (backup) database aktif..."
if [ -f backup_db.sh ]; then
    bash backup_db.sh || true
fi

# 3. Terapkan database baru hasil git pull ke folder persistensi docker (Pertahankan password EC2)
if [ -f studio_ml.db ]; then
    echo "📋 Menyalin database baru ke data/studio_ml.db..."
    mkdir -p data
    if [ -f data/studio_ml.db ]; then
        python3 -c "
import sqlite3, shutil
try:
    c_dest = sqlite3.connect('data/studio_ml.db')
    pw_rows = c_dest.execute('SELECT username, password_hash FROM admin_users').fetchall()
    c_dest.close()
    shutil.copy2('studio_ml.db', 'data/studio_ml.db')
    if pw_rows:
        c_new = sqlite3.connect('data/studio_ml.db')
        for u, p in pw_rows:
            c_new.execute('UPDATE admin_users SET password_hash = ? WHERE username = ?', (p, u))
        c_new.commit()
        c_new.close()
        print('🔒 Password guru aktif di EC2 berhasil dipertahankan.')
except Exception:
    shutil.copy2('studio_ml.db', 'data/studio_ml.db')
" 2>/dev/null || cp studio_ml.db data/studio_ml.db
    else
        cp studio_ml.db data/studio_ml.db
    fi
    echo "✅ Database baru berhasil disalin!"
fi

# 4. Bangun ulang / restart kontainer Docker
echo "🚀 Menerapkan perubahan ke kontainer Docker..."
sudo docker compose down 2>/dev/null || true
sudo docker compose up -d --build

echo "========================================================="
echo "🎉 UPDATE BERHASIL!"
echo "Aplikasi dan database baru (41 siswa, kuis baru, modul baru) sudah aktif di EC2."
echo "Status kontainer: sudo docker compose ps"
echo "========================================================="
