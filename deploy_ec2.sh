#!/bin/bash
# ==============================================================================
# Script Otomatisasi Deployment Studio ML & E-Learning SMK ke AWS EC2 (Ubuntu)
# ==============================================================================

set -e

echo "========================================================="
echo "🚀 Memulai Konfigurasi Server AWS EC2 untuk Studio ML..."
echo "========================================================="

# 1. Update paket & dependensi dasar
echo "📦 Memperbarui paket sistem Ubuntu..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git ufw

# 2. Setup SWAP Memory 2GB (Sangat Penting untuk EC2 Free Tier RAM 1GB)
if [ ! -f /swapfile ]; then
    echo "🧠 Mengatur Swap Memory 2GB agar RAM 1GB tidak kehabisan memori..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swap memory 2GB berhasil diaktifkan!"
else
    echo "ℹ️ Swap file sudah ada, melewati langkah swap."
fi

# 3. Install Docker & Docker Compose jika belum ada
if ! command -v docker &> /dev/null; then
    echo "🐳 Menginstal Docker & Docker Compose Plugin..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo apt install -y docker-compose-plugin
    rm get-docker.sh
    echo "✅ Docker berhasil diinstal!"
else
    echo "ℹ️ Docker sudah terinstal."
fi

# 4. Siapkan folder data persistensi SQLite
echo "📁 Menyiapkan folder data persistensi..."
mkdir -p data
if [ -f studio_ml.db ] && [ ! -f data/studio_ml.db ]; then
    echo "📋 Menyalin data awal studio_ml.db ke data/studio_ml.db..."
    cp studio_ml.db data/studio_ml.db
fi

# 5. Jalankan Aplikasi menggunakan Docker Compose
echo "🚀 Membangun dan menyalakan container aplikasi..."
sudo docker compose down 2>/dev/null || true
sudo docker compose up -d --build

# 6. Dapatkan IP Public server
PUBLIC_IP=$(curl -s https://checkip.amazonaws.com || curl -s ifconfig.me || echo "IP_SERVER_ANDA")

echo "========================================================="
echo "🎉 DEPLOYMENT BERHASIL!"
echo "Aplikasi Studio ML & E-Learning CBT SMK aktif."
echo ""
echo "🌐 Akses Web Siswa & Guru:"
echo "   http://${PUBLIC_IP}"
echo ""
echo "📊 Cek status kontainer: sudo docker compose ps"
echo "📜 Cek logs real-time  : sudo docker compose logs -f"
echo "🔄 Restart aplikasi    : sudo docker compose restart"
echo "========================================================="
