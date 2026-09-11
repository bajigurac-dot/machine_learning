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
git pull origin main

# 2. Backup database yang saat ini sedang aktif di EC2
echo "💾 Membuat salinan cadangan (backup) database aktif..."
if [ -f backup_db.sh ]; then
    bash backup_db.sh || true
fi

# 3. Terapkan database baru hasil git pull ke folder persistensi docker
if [ -f studio_ml.db ]; then
    echo "📋 Menyalin database baru ke data/studio_ml.db..."
    mkdir -p data
    cp studio_ml.db data/studio_ml.db
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
