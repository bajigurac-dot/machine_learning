import json
import datetime
import requests

def generate_local_prd(project_name, dataset_name=None, task_type=None, target_col=None):
    """Menghasilkan PRD & Lembar Kerja Praktikum Siswa SMK berbasis kecerdasan lokal."""
    dataset_name = dataset_name or "Dataset Kustom"
    task_type = task_type or "Klasifikasi/Regresi"
    target_col = target_col or "Target"
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    return f"""# 📄 Lembar Rencana Proyek & PRD Pembelajaran Siswa SMK
## Proyek: {project_name}

- **Pengembang / Instruktur**: Thoriq Azis
- **Tanggal Pelaksanaan**: {today}
- **Target Pembelajar**: Siswa SMK Jurusan RPL / TKJ / SIJA
- **Topik Pembelajaran**: Pemrograman Python & Machine Learning ({task_type.capitalize()})
- **Alat Pengembangan**: Visual Studio Code (VS Code), Python 3.11+, Terminal
- **Dataset Praktik**: `{dataset_name}` (Variabel Target: `{target_col}`)

---

### 1. Tujuan Pembelajaran & Capaian Kompetensi
Setelah menyelesaikan proyek praktikum ini, siswa SMK diharapkan mampu:
1. Memahami konsep dasar pemodelan Machine Learning dan pra-pemrosesan data tabular.
2. Menulis dan mengorganisir skrip Python modular menggunakan VS Code.
3. Menjalankan program dan mengamati log output melalui Terminal terintegrasi VS Code.
4. Mengevaluasi akurasi model serta melakukan inferensi uji coba mandiri.

---

### 2. Alat & Bahan Praktikum di Lab Komputer
- **Laptop / PC**: RAM minimal 4GB, OS Windows / Linux.
- **Visual Studio Code (VS Code)**: Sudah terinstal ekstensi resmi *"Python"* dari Microsoft.
- **Python & Libraries**:
  ```bash
  pip install pandas numpy scikit-learn
  ```
- **Dataset**: File `{dataset_name}.csv` ditempatkan dalam 1 folder proyek yang sama.

---

### 3. Alur Kerja Praktik Mandiri Siswa (Step-by-Step di VS Code)

#### Langkah 1: Persiapan Folder Proyek
1. Buat folder baru di komputer, misal: `D:\\Praktikum_SMK\\Proyek_{target_col}`.
2. Buka folder tersebut di VS Code (**File -> Open Folder**).
3. Buat file baru bernama **`main.py`**.

#### Langkah 2: Implementasi Skrip Python (`main.py`)
Salin kode berikut ke dalam file `main.py` di VS Code:

```python
# ==========================================================
# Praktikum Machine Learning Mandiri Siswa SMK
# File: main.py | Target: {target_col}
# ==========================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print(">>> [Langkah 1] Membaca data {dataset_name}.csv...")
df = pd.read_csv("{dataset_name}.csv").dropna()

# Pisahkan fitur dan target
X = df.drop(columns=["{target_col}"]).select_dtypes(include=[np.number])
y = df["{target_col}"]

print(">>> [Langkah 2] Membagi data train & test (80:20)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(">>> [Langkah 3] Melatih model Machine Learning...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(">>> [Langkah 4] Menguji performa...")
y_pred = model.predict(X_test)
print(f"\\n🎯 HASIL AKURASI: {{accuracy_score(y_test, y_pred) * 100:.2f}}%")
print(">>> Praktikum Berhasil Diselesaikan!")
```

#### Langkah 3: Eksekusi Terminal di VS Code
1. Buka Terminal terintegrasi di VS Code (**Ctrl + `**).
2. Jalankan perintah:
   ```bash
   python main.py
   ```
3. Catat angka akurasi yang berhasil diperoleh!

---

### 4. Rubrik Penilaian Mandiri Siswa SMK (Self-Assessment)
| No | Kriteria Unjuk Kerja | Status |
|---|---|---|
| 1 | Berhasil membuat file `main.py` di VS Code | [ ] Tuntas |
| 2 | Berhasil menjalankan skrip via terminal tanpa error | [ ] Tuntas |
| 3 | Mampu menjelaskan fungsi `train_test_split` | [ ] Tuntas |
| 4 | Berhasil memodifikasi parameter `n_estimators` | [ ] Tuntas |

---
*Dokumen ini dapat diunduh dalam format Markdown (.md) untuk dijadikan Jobsheet / Lembar Tugas Siswa.*
"""

def generate_local_feature_spec(feature_name, goal, target_user, complexity, current_context=None):
    """Menghasilkan Technical Feature Specification dan Task Breakdown terperinci."""
    current_context = current_context or {}
    dataset = current_context.get("dataset_name", "Data Proyek")
    task_type = current_context.get("task_type", "Machine Learning")
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    return f"""# Spesifikasi Teknis Fitur (Feature Spec & Task Breakdown)
## Fitur: {feature_name}

- **Tanggal**: {today}
- **Target Pengguna**: {target_user or "End-User & Tim Teknis"}
- **Tingkat Kompleksitas**: {complexity.upper()}
- **Tujuan Utama**: {goal or "Meningkatkan kemampuan fungsional sistem Machine Learning"}
- **Konteks Sistem**: Proyek {dataset} ({task_type})

---

### 1. Gambaran Umum (Overview) & Value Proposition
Fitur **{feature_name}** dirancang untuk memenuhi kebutuhan: *{goal}*. Fitur ini memberikan dampak langsung kepada *{target_user}* dengan menyederhanakan alur kerja kompleks menjadi langkah yang intuitif dan terukur.

### 2. User Stories
* **Sebagai seorang** {target_user or "pengguna aplikasi"},
* **Saya ingin** {goal.lower() if goal else f"menggunakan fitur {feature_name}"},
* **Sehingga** saya dapat meningkatkan produktivitas dan mendapatkan hasil prediksi yang akurat tanpa hambatan teknis.

### 3. Kriteria Keberhasilan (Acceptance Criteria - Gherkin Syntax)
```gherkin
Skenario 1: Eksekusi Berhasil (Happy Path)
  Dengan (Given) Pengguna telah berada di halaman {feature_name}
  Ketika (When) Pengguna memasukkan parameter yang valid dan menekan tombol konfirmasi
  Maka (Then) Sistem memproses data dalam waktu < 2 detik
  Dan (And) Sistem menampilkan hasil visual yang jelas serta memberikan feedback sukses

Skenario 2: Validasi Error & Input Tidak Valid
  Dengan (Given) Pengguna memasukkan data yang tidak sesuai format
  Ketika (When) Permintaan dikirim ke server
  Maka (Then) Sistem menampilkan pesan kesalahan yang ramah pengguna (user-friendly alert)
  Dan (And) Proses tidak menyebabkan crash atau kegagalan sistem
```

### 4. Arsitektur & Skema Komponen
* **Frontend Layer**: Komponen UI interaktif dengan validasi form klien, indikator loading progresif, dan penampil data visual.
* **API Endpoints**:
  * `POST /api/{feature_name.lower().replace(' ', '_')}`: Menerima payload input.
  * `GET /api/{feature_name.lower().replace(' ', '_')}/status`: Memeriksa status proses komputasi.
* **Backend Processing**: Logika pemrosesan di Python menggunakan pandas & scikit-learn terisolasi dalam try-catch exception handling.

### 5. Rincian Pembagian Tugas & Roadmap Sprint (Sprint Task Breakdown)
Rencana implementasi diatur dalam alur **Sprint Praktikum (Sprint 1 & Sprint 2)**:

#### A. Backend & Data Engine (Sprint 1)
- [ ] **BE-01**: Desain endpoint API di Flask dengan validasi payload JSON *(Estimasi: 3 Story Points)*
- [ ] **BE-02**: Implementasi logika pengolahan data & pemanggilan fungsi scikit-learn *(Estimasi: 5 Story Points)*
- [ ] **BE-03**: Pembuatan unit test pada `tests/` dengan coverage > 85% *(Estimasi: 2 Story Points)*

#### B. Frontend & User Experience
- [ ] **FE-01**: Pembuatan layout UI responsif, modern glassmorphic card, dan input controls *(Estimasi: 3 Story Points)*
- [ ] **FE-02**: Integrasi state management dan komunikasi AJAX/Fetch ke endpoint backend *(Estimasi: 3 Story Points)*
- [ ] **FE-03**: Penanganan animasi transisi, feedback alert, dan modal konfirmasi *(Estimasi: 2 Story Points)*

#### C. Testing & QA (Quality Assurance)
- [ ] **QA-01**: Pengujian fungsional skenario Happy Path dan Edge Cases *(Estimasi: 2 Story Points)*
- [ ] **QA-02**: Pengujian performa beban latensi respons di bawah 500ms *(Estimasi: 1 Story Point)*

---
*Dihasilkan oleh Studio ML AI Copilot. Siap diekspor ke Jira / GitHub Issues / Trello.*
"""

PREFERRED_GEMINI_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-1.5-flash"
]

def test_gemini_connection(api_key):
    """Menguji keabsahan API Key dan koneksi langsung ke Google Gemini API."""
    if not api_key:
        return {"success": False, "error": "API Key belum diisi."}
    
    last_error = None
    for model_name in PREFERRED_GEMINI_MODELS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": "PONG: verifikasi koneksi."}]}]
            }
            resp = requests.post(url, json=payload, timeout=8)
            if resp.status_code == 200:
                return {
                    "success": True, 
                    "message": f"Koneksi Berhasil! Model Google {model_name} aktif dan siap digunakan.",
                    "model": model_name
                }
            elif resp.status_code in [404, 429, 503]:
                # Model busy or superseded, try next model in pool
                continue
            else:
                err_data = resp.json() if resp.text else {}
                err_msg = err_data.get("error", {}).get("message", f"HTTP {resp.status_code}: Permintaan ditolak")
                return {"success": False, "error": err_msg}
        except Exception as e:
            last_error = str(e)
            
    return {"success": False, "error": last_error or "Gagal menghubungi server Gemini"}

def handle_ai_chat(message, conversation_history=None, current_context=None, api_key=None, provider="local", return_dict=False):
    """
    Menangani chat interaktif dengan AI mengenai PRD, fitur, dan task.
    Mendukung mode cerdas offline (local) atau LLM eksternal jika API key disediakan.
    """
    conversation_history = conversation_history or []
    current_context = current_context or {}
    
    msg_lower = message.lower()
    provider_used = "local"
    gemini_error = None
    
    # Check if external Gemini API is requested and provided
    if provider == "gemini" and api_key:
        for model_name in PREFERRED_GEMINI_MODELS:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                system_instruction = (
                    "Anda adalah Thoriq Azis, Guru & Mentor Pemrograman Python dan Machine Learning yang ramah, komunikatif, dan sangat peduli "
                    "pada pemahaman siswa SMK (Sekolah Menengah Kejuruan jurusan RPL / TKJ / SIJA / Rekayasa Perangkat Lunak). "
                    "Tujuan utama Anda adalah membimbing siswa belajar coding Python dan AI secara mandiri dan langsung mempraktikkannya di VS Code (Visual Studio Code).\\n\\n"
                    "Setiap kali siswa bertanya (misal tentang Looping/Perulangan, Percabangan If-Else, Fungsi/Def, List/Dict, Pandas, atau Machine Learning):\\n"
                    "1. Berikan PENJELASAN KONSEP DENGAN ANALOGI MUDAH yang dekat dengan kehidupan sehari-hari anak muda.\\n"
                    "2. Berikan SKRIP KODE PYTHON LENGKAP & BERSIH yang diberi komentar penjelasan di setiap baris penting.\\n"
                    "3. Berikan PANDUAN LANGKAH DEMI LANGKAH MENJALANKANNYA DI VS CODE:\\n"
                    "   - Nama file yang disarankan (contoh: latihan_looping.py)\\n"
                    "   - Cara buat file & paste kode di VS Code\\n"
                    "   - Cara buka terminal terintegrasi di VS Code (tekan tombol Ctrl + `)\\n"
                    "   - Perintah terminal untuk menjalankannya (python nama_file.py)\\n"
                    "   - Cara membaca output terminal\\n"
                    "4. Berikan 1 TANTANGAN PRAKTIK MANDIRI (Hands-on Challenge) agar siswa mencoba memodifikasi kodenya sendiri di VS Code!\\n"
                    "Gunakan gaya bahasa yang suportif dan antusias."
                )
                contents = []
                for h in conversation_history[-6:]:
                    role = "user" if h.get("role") == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": h.get("content", "")}]})
                contents.append({"role": "user", "parts": [{"text": f"Konteks Proyek: {json.dumps(current_context)}\\nPertanyaan Siswa: {message}"}]})
                
                resp = requests.post(url, json={"contents": contents, "systemInstruction": {"parts": [{"text": system_instruction}]}}, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0]["content"]["parts"][0]["text"]
                        if return_dict:
                            return {"reply": text, "provider_used": f"gemini ({model_name})", "gemini_error": None}
                        return text
                elif resp.status_code in [404, 429, 503]:
                    # Model not found or temporary load spike, immediately fallback to next model
                    err_data = resp.json() if resp.text else {}
                    gemini_error = err_data.get("error", {}).get("message", f"HTTP {resp.status_code}")
                    continue
                else:
                    err_data = resp.json() if resp.text else {}
                    gemini_error = err_data.get("error", {}).get("message", f"HTTP {resp.status_code}")
                    break
            except Exception as e:
                gemini_error = str(e)

    # Expert Local Rules Engine: Khusus Siswa SMK Siap Praktik di VS Code
    dataset_name = current_context.get("dataset_name", "Dataset Proyek")
    target_col = current_context.get("target_column", "Target")
    task_type = current_context.get("task_type", "Klasifikasi")
    best_model = current_context.get("best_model", "Random Forest")
    best_score = current_context.get("best_score", "Tinggi")
    
    # 1. Topik: Looping / Perulangan (For & While)
    if "loop" in msg_lower or "perulangan" in msg_lower or "for " in msg_lower or "while" in msg_lower:
        result_text = """### 🔄 Materi Praktik: Perulangan (Looping) di Python

Halo sobat siswa SMK! Bersama mentor **Thoriq Azis**, mari kita pelajari konsep **Looping (Perulangan)**.
*Analogi: Seperti lari keliling lapangan upacara sebanyak 5 putaran. Kamu menghitung putaran ke-1, ke-2, sampai ke-5 lalu berhenti.*

Di Python ada 2 jenis looping utama:
1. **`for loop`**: Digunakan jika jumlah putaran/perulangannya sudah kita ketahui pasti.
2. **`while loop`**: Digunakan jika perulangan terus berjalan selama suatu kondisi masih benar (`True`).

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_looping.py`)
```python
# ==========================================================
# Latihan Looping Python - Belajar Bersama Thoriq Azis
# Instruktur: Thoriq Azis | File: latihan_looping.py
# ==========================================================

print("=== 1. CONTOH FOR LOOP (Hitung Putaran Lapangan) ===")
# range(1, 6) artinya mulai dari angka 1 sampai 5
for putaran in range(1, 6):
    print(f"Semangat! Siswa sedang lari putaran ke-{putaran}")

print("\\n=== 2. CONTOH FOR LOOP DENGAN DAFTAR DATA (LIST) ===")
jurusan_smk = ["RPL", "TKJ", "SIJA"]
for nama_jurusan in jurusan_smk:
    print(f"Jurusan Unggulan: {nama_jurusan}")

print("\\n=== 3. CONTOH WHILE LOOP (Hitung Mundur Roket) ===")
hitungan = 5
while hitungan > 0:
    print(f"Peluncuran dalam: {hitungan}...")
    hitungan -= 1  # kurangi 1 setiap putaran agar tidak infinite loop

print("ROKET MELUNCUR KE LUAR ANGKASA! 🚀")
```

---

#### 💻 Panduan Langkah demi Langkah Menjalankan di VS Code:
1. **Buka VS Code** di laptop/komputer Anda.
2. Klik menu **File** -> **New File**, simpan dengan nama **`latihan_looping.py`** di folder belajar Anda.
3. Salin (*copy*) skrip kode di atas dan tempel (*paste*) ke dalam file tersebut, lalu simpan (**Ctrl + S**).
4. Buka terminal di VS Code dengan menekan tombol kombinasi **`Ctrl + \``** (atau menu **Terminal** -> **New Terminal**).
5. Pada terminal, ketik perintah:
   ```bash
   python latihan_looping.py
   ```
   *(atau `python3 latihan_looping.py` jika di macOS/Linux)*
6. Tekan **Enter** dan perhatikan output yang muncul di terminal!

---

#### 🎯 Tantangan Praktik Mandiri (Coba Sendiri!):
Modifikasi kode di atas agar:
1. Menampilkan deret bilangan genap dari **2 sampai 20** menggunakan `for loop`! (*Petunjuk: gunakan `range(2, 21, 2)`*).
2. Buat daftar 5 nama teman sekelasmu di dalam list, lalu tampilkan sapaan *"Halo [Nama Teman]!"* menggunakan perulangan!
"""

    # 2. Topik: Percabangan (If - Else)
    elif "if" in msg_lower or "percabangan" in msg_lower or "kondisi" in msg_lower or "else" in msg_lower:
        result_text = """### 🔀 Materi Praktik: Percabangan (If - Else) di Python

Halo sobat SMK! **Percabangan (If - Else)** adalah cara kita mengajarkan komputer untuk mengambil keputusan berdasarkan kondisi tertentu.
*Analogi: Jika lampu lalu lintas berwarna HIJAU, maka motor maju. Jika MERAH, maka motor berhenti!*

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_kondisi.py`)
```python
# ==========================================================
# Latihan Percabangan Nilai Kelulusan SMK
# File: latihan_kondisi.py
# ==========================================================

print("=== SISTEM PENENTU PREDIKAT NILAI SISWA SMK ===")

# Input nilai dari pengguna (diubah ke tipe angka float/int)
nama_siswa = input("Masukkan Nama Siswa: ")
nilai_kejuruan = float(input("Masukkan Nilai Ujian Praktik (0-100): "))

# Logika Percabangan If - Elif - Else
if nilai_kejuruan >= 90:
    predikat = "A (Sangat Kompeten / Luar Biasa!)"
    keterangan = "Selamat! Anda siap magang di industri tier-1."
elif nilai_kejuruan >= 78:
    predikat = "B (Kompeten)"
    keterangan = "Bagus! Anda lulus standar kompetensi kejuruan."
elif nilai_kejuruan >= 65:
    predikat = "C (Cukup)"
    keterangan = "Lulus bersyarat. Perlu menambah latihan praktik mandiri."
else:
    predikat = "D (Belum Kompeten)"
    keterangan = "Harap mengikuti ujian remedial bersama guru pembimbing."

print("\\n---------------- HASIL EVALUASI ----------------")
print(f"Siswa     : {nama_siswa}")
print(f"Nilai     : {nilai_kejuruan}")
print(f"Predikat  : {predikat}")
print(f"Pesan     : {keterangan}")
```

---

#### 💻 Panduan Menjalankan di VS Code:
1. Buat file baru di VS Code dengan nama **`latihan_kondisi.py`**.
2. Tempel kode di atas lalu simpan (**Ctrl + S**).
3. Buka Terminal terintegrasi di VS Code (**Ctrl + `**).
4. Jalankan perintah:
   ```bash
   python latihan_kondisi.py
   ```
5. Ketik nama dan nilai saat terminal meminta input, lalu tekan **Enter**!

---

#### 🎯 Tantangan Praktik Mandiri:
Tambahkan kondisi jika nilai di atas 100 atau di bawah 0, program akan menampilkan pesan: *"Input tidak valid! Nilai harus antara 0 - 100."*
"""

    # 3. Topik: Fungsi (Def)
    elif "fungsi" in msg_lower or "def " in msg_lower or "function" in msg_lower:
        result_text = """### 📦 Materi Praktik: Membuat Fungsi (`def`) di Python

Halo sobat SMK! **Fungsi (Function)** adalah blok kode terstruktur yang kita beri nama agar bisa dipanggil berulang kali tanpa mengetik ulang rumusnya.
*Analogi: Seperti tombol BLENDER. Kamu memasukkan buah (input/parameter), blender memprosesnya, dan mengeluarkan jus segar (output/return).*

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_fungsi.py`)
```python
# ==========================================================
# Latihan Fungsi Matematika & Kasir Sederhana SMK
# File: latihan_fungsi.py
# ==========================================================

# 1. Fungsi sederhana tanpa parameter
def sambutan():
    print("==========================================")
    print("   SELAMAT DATANG DI LAB KOMPUTER SMK     ")
    print("==========================================")

# 2. Fungsi dengan parameter dan nilai kembalian (return)
def hitung_diskon_siswa(total_belanja, persen_diskon=10):
    \"\"\"Menghitung potongan harga khusus kartu pelajar SMK\"\"\"
    potongan = total_belanja * (persen_diskon / 100)
    total_akhir = total_belanja - potongan
    return total_akhir, potongan

# Program Utama
sambutan()

belanja = 150000
bayar, hemat = hitung_diskon_siswa(belanja, 15)

print(f"Total Belanja Awal   : Rp {belanja:,}")
print(f"Hemat Diskon Pelajar : Rp {hemat:,.0f}")
print(f"Total yang Dibayar   : Rp {bayar:,.0f}")
```

---

#### 💻 Cara Praktik di VS Code:
1. Buat file **`latihan_fungsi.py`** di VS Code.
2. Buka terminal (**Ctrl + `**) dan jalankan: `python latihan_fungsi.py`.
3. Amati bagaimana fungsi `hitung_diskon_siswa` mengembalikan nilai yang rapi!
"""

    # 4. Topik: List & Dictionary
    elif "list" in msg_lower or "dict" in msg_lower or "array" in msg_lower:
        result_text = """### 📑 Materi Praktik: Struktur Data (List & Dictionary)

Halo sobat SMK! **List** dan **Dictionary** adalah wadah untuk menyimpan kumpulan data di Python:
- **`List [ ]`**: Menyimpan daftar berurutan (misal: daftar nama siswa).
- **`Dictionary { }`**: Menyimpan pasangan Kunci & Nilai (*Key: Value*, misal: identitas lengkap siswa).

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_data.py`)
```python
# ==========================================================
# Manajemen Data Siswa Kelas SMK
# File: latihan_data.py
# ==========================================================

# 1. List (Daftar)
mata_pelajaran = ["Pemrograman Dasar", "Basis Data", "PBO", "Machine Learning"]
print("Daftar Mapel Kejuruan:", mata_pelajaran)
mata_pelajaran.append("Cloud Computing") # Tambah mapel baru

# 2. Dictionary (Data Terstruktur Kunci-Nilai)
profil_siswa = {
    "nisn": "0051234567",
    "nama": "Thoriq Azis",
    "kelas": "XII RPL 1",
    "jurusan": "Rekayasa Perangkat Lunak",
    "nilai": [88, 92, 85, 90]
}

print(f"\\nNama Siswa : {profil_siswa['nama']}")
print(f"Kelas      : {profil_siswa['kelas']}")

# Menghitung rata-rata nilai dari list di dalam dictionary
rata_rata = sum(profil_siswa['nilai']) / len(profil_siswa['nilai'])
print(f"Rata-rata Nilai : {rata_rata:.1f}")
```

---

#### 💻 Cara Menjalankan di VS Code:
Simpan sebagai **`latihan_data.py`** di VS Code, lalu ketik `python latihan_data.py` di terminal!
"""

    # 5. Topik: PRD / Jobsheet Praktikum Siswa SMK
    elif "prd" in msg_lower or "jobsheet" in msg_lower or "lembar kerja" in msg_lower:
        result_text = generate_local_prd(f"Praktikum Python & ML: Prediksi {target_col}", dataset_name, task_type, target_col)

    # 6. Topik: Machine Learning Pertama di VS Code
    elif "machine learning" in msg_lower or "ml" in msg_lower or "model" in msg_lower:
        result_text = f"""### 🤖 Praktikum Machine Learning Pertama di VS Code untuk Siswa SMK

Selamat datang di dunia AI, sobat SMK! Proyek aktif kita menggunakan dataset **`{dataset_name}`** dengan target **`{target_col}`**.

Model terbaik yang ditemukan oleh AutoML Studio adalah **{best_model}** dengan performa **{best_score}**.

---

#### 🐍 Skrip Python Siap Jalankan di VS Code (`proyek_ml_smk.py`)
```python
# ==========================================================
# Proyek Machine Learning Siswa SMK
# Dataset: {dataset_name} | Model: {best_model}
# ==========================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("1. Memuat dataset...")
# Pastikan file CSV berada di folder yang sama dengan file skrip ini
df = pd.read_csv("{dataset_name}.csv")

# Tentukan target dan fitur
target = "{target_col}"
X = df.drop(columns=[target]).select_dtypes(include=['number']).fillna(0)
y = df[target]

print("2. Membagi data menjadi Train (80%) dan Test (20%)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("3. Melatih model Machine Learning...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("4. Menguji akurasi model...")
prediksi = model.predict(X_test)
skor = accuracy_score(y_test, prediksi)
print(f"\\n🎯 HASIL AKURASI MODEL: {{skor * 100:.2f}}%")
print("Selamat! Model Machine Learning Anda berhasil bekerja di VS Code!")
```

---

#### 💻 Langkah Menjalankan di VS Code:
1. Klik tab **`🐍 Kode Python`** di menu samping untuk mengunduh kode lengkap atau salin kode di atas.
2. Simpan di folder proyek VS Code dengan nama **`proyek_ml_smk.py`**.
3. Buka Terminal di VS Code (**Ctrl + `**), pastikan library sudah terinstal:
   ```bash
   pip install pandas scikit-learn
   ```
4. Jalankan program:
   ```bash
   python proyek_ml_smk.py
   ```
5. Amati angka akurasi yang dicetak di terminal!
"""

    # 7. Topik: Task Breakdown & Sprint Roadmap Praktikum
    elif "task" in msg_lower or "sprint" in msg_lower or "spec" in msg_lower:
        result_text = generate_local_feature_spec(
            feature_name="Praktikum Mandiri Python di VS Code",
            goal="Menyelesaikan latihan pemrograman Python dan mini ML secara bertahap",
            target_user="Siswa SMK & Guru Pembimbing",
            complexity="Medium",
            current_context=current_context
        )

    else:
        result_text = f"""### 🎓 Halo Sobat SMK! AI Mentor Python Siap Membantu

Saya adalah asisten AI yang siap memandu Anda belajar Python dan Machine Learning dari dasar hingga mahir untuk langsung dipraktikkan di **Visual Studio Code (VS Code)**!

Ketik materi yang ingin Anda pelajari atau klik pintasan di atas:
1. 🔄 **Ketik "Belajar Looping"**: Panduan lengkap perulangan `for` dan `while` + contoh kasus + tantangan mandiri.
2. 🔀 **Ketik "Belajar Percabangan"**: Logika `if-elif-else` penentu kelulusan nilai siswa SMK.
3. 📦 **Ketik "Belajar Fungsi"**: Cara membuat fungsi `def` yang rapi dan modular.
4. 📑 **Ketik "Belajar List & Dict"**: Pengelolaan struktur data siswa.
5. 🤖 **Ketik "Buat Model ML"**: Langkah membuat skrip Machine Learning mandiri di VS Code.
6. 📄 **Ketik "Buatkan PRD / Jobsheet"**: Menghasilkan Lembar Kerja Praktikum Proyek Siswa SMK siap cetak!

*Setiap jawaban dilengkapi skrip kode bersih dan panduan langkah eksekusi terminal di VS Code!*
"""

    if return_dict:
        return {
            "reply": result_text,
            "provider_used": "local",
            "gemini_error": gemini_error
        }
    return result_text
