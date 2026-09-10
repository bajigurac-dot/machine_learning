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
                    "Setiap kali siswa bertanya (misal tentang Looping/Perulangan, Percabangan If-Else, Fungsi/Def, List/Dict, Basis Data & Query SQL SQLite, Pandas, atau Machine Learning):\\n"
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
    import re
    clean_msg = msg_lower.strip()
    
    has_specific_subtopic = any(
        sub in clean_msg for sub in [
            "loop", "ulang", "while", "for ", "percabangan", "kondisi", "if", "else", 
            "input", "keyboard", "print", "cetak", "variabel", "variable", "tipe data",
            "list", "dict", "array", "fungsi", "def", "error", "try", "except", 
            "machine learning", "ml", "database", "sql", "sqlite", "mysql", "query", "tabel",
            "table", "rdbms", "select", "insert", "update", "delete", "crud", "join",
            "prd", "jobsheet", "latihan 1", "latihan 2", "latihan 3", "latihan 4", "latihan 5",
            "latihan 6", "latihan 7", "latihan 8", "latihan 9", "latihan 10", "latihan 11",
            "titanic", "iris", "salary", "gaji", "churn", "diabetes", "housing", "rumah", "dataset", "data contoh"
        ]
    )

    # 0. Topik 0: Pengenalan Bahasa Pemrograman Python (Umum)
    if not has_specific_subtopic and (
        clean_msg in ["python", "apa itu python", "belajar python", "pengenalan python", "tentang python", "kenapa python", "materi python", "sejarah python", "halo python"]
        or bool(re.search(r"^(apa\s*itu\s*python|belajar\s*python|pengenalan\s*python|tentang\s*python|kenapa\s*python|mengapa\s*python|keunggulan\s*python|pengantar\s*python|halo\s*python)$", clean_msg))
        or ("python" in clean_msg and any(w in clean_msg for w in ["apa itu", "pengenalan", "kenapa", "mengapa", "sejarah", "keunggulan", "belajar", "kegunaan", "mulai"]))
    ):
        result_text = """### 🐍 Pengenalan Bahasa Pemrograman Python untuk Siswa SMK

Halo sobat siswa SMK! Bersama mentor **Thoriq Azis, S.Kom**, selamat datang di dunia pemrograman modern bersama **Python**!
*Analogi: Jika bahasa mesin kuno seperti instruksi teknis rumit yang sulit dipahami manusia, Python diciptakan seperti bahasa percakapan sehari-hari yang sangat ringkas, intuitif, dan mudah dipelajari.*

#### 💡 Mengapa Siswa SMK Wajib Menguasai Python?
1. **Sintaks Paling Bersih & Elegan**: Tidak membutuhkan titik koma (`;`) di setiap akhir baris atau kurung kurawal (`{}`) berbelit-belit. Python menggunakan indentasi (spasi/Tab) yang melatih siswa menulis kode rapi.
2. **Bahasa Pemrograman #1 di Dunia**: Menurut indeks TIOBE & GitHub, Python adalah bahasa terpopuler di dunia kerja untuk:
   - **Artificial Intelligence & Machine Learning**: Scikit-Learn, PyTorch, TensorFlow.
   - **Data Science & Analisis Basis Data**: Pandas, NumPy, Matplotlib, SQLite, MySQL.
   - **Backend Web Development**: Flask, Django, FastAPI.
   - **Otomatisasi Sistem & Jaringan Komputer (TKJ/SIJA)**: Scripting administrasi server, bot, API.
3. **Ekosistem & Komunitas Terbesar**: Jutaan modul pustaka (*libraries*) siap pakai secara gratis.

---

#### 🐍 Skrip Perdana Python Anda (`halo_python.py`)
```python
# ==========================================================
# Pengenalan Bahasa Python Siswa SMK Cahaya Pertiwi
# Instruktur: Thoriq Azis | File: halo_python.py
# ==========================================================

nama_siswa = "Sobat Siswa SMK"
jurusan = "Rekayasa Perangkat Lunak (RPL)"
sekolah = "SMK Cahaya Pertiwi"

print("=" * 55)
print(f"🎉 SELAMAT DATANG DI DUNIA CODING PYTHON, {nama_siswa.upper()}!")
print(f"Sekolah : {sekolah}")
print(f"Jurusan : {jurusan}")
print("=" * 55)

# Contoh kemampuan Python: Perhitungan & Looping singkat
print("\\n5 Keunggulan Utama Python:")
keunggulan = [
    "1. Mudah dipelajari pemula & sintaks mirip bahasa manusia",
    "2. Bahasa utama Artificial Intelligence & Machine Learning",
    "3. Dukungan basis data (SQLite, MySQL, PostgreSQL) sangat kuat",
    "4. Kompatibel di semua OS (Windows, Linux, macOS)",
    "5. Komunitas developer terbesar dan teraktif di dunia"
]

for item in keunggulan:
    print(f"  ✓ {item}")

print("\\n>>> Semangat belajar! Anda siap menjadi Programmer & AI Engineer masa depan.")
```

---

#### 💻 Panduan Menjalankannya di VS Code:
1. Buka **VS Code** di komputer Anda.
2. Buat file baru bernama **`halo_python.py`** (**File -> New File** lalu simpan dengan **Ctrl + S**).
3. Salin kode di atas lalu simpan.
4. Buka Terminal terintegrasi VS Code (**Ctrl + `**).
5. Jalankan perintah:
   ```bash
   python halo_python.py
   ```

---

#### 🗺️ Peta Kurikulum Belajar Python & Database di AI Tutor SMK:
Ketik angka materi untuk langsung mempelajari modul yang diinginkan:
- 📢 **Ketik "1"**: Cetak Teks (`print()`)
- 🏷️ **Ketik "2"**: Variabel & Tipe Data
- ⌨️ **Ketik "3"**: Input Keyboard & Aritmatika
- 🔀 **Ketik "4"**: Percabangan `if - else`
- 🔄 **Ketik "5"**: Perulangan `for` & `while`
- 📑 **Ketik "6"**: List & Dictionary
- 📦 **Ketik "7"**: Fungsi Modular `def`
- 🛡️ **Ketik "8"**: Penanganan Error `try - except`
- 🤖 **Ketik "9"**: Praktikum Machine Learning
- 📄 **Ketik "10"**: Jobsheet PRD Praktikum
- 🗄️ **Ketik "11"**: Basis Data & Query SQL (SQLite & MySQL)
"""

    # 1. Topik 1: Cetak Teks (print) & Format Output
    elif (bool(re.search(r"\bprint\b|\bcetak\b|hello\s*world|materi\s*1|dasar\s*1", msg_lower)) and "sprint" not in msg_lower) or clean_msg in ["1", "materi 1", "modul 1"]:
        result_text = """### 📢 Materi Dasar 1: Cetak Teks ke Layar (`print`) di Python

Halo sobat siswa SMK! Bersama mentor **Thoriq Azis**, mari kita mulai langkah pertama pemrograman dari hal paling fundamental: **Mencetak Teks ke Layar**.
*Analogi: Seperti mikrofon dan papan pengumuman sekolah. Fungsi `print()` bertugas menyampaikan dan menampilkan pesan dari komputer kepada kita.*

#### 💡 Poin-Poin Penting:
1. Teks harus selalu diapit tanda kutip dua (`"..."`) atau kutip satu (`'...'`).
2. Angka bisa langsung dicetak tanpa tanda kutip.
3. Gunakan `\\n` untuk membuat baris baru (*new line*) dan `\\t` untuk spasi tab.
4. Gunakan **f-string** (`f"Halo {nama}"`) untuk menyisipkan variabel ke dalam kalimat dengan mudah.

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_1_print.py`)
```python
# ==========================================================
# Materi 1: Belajar Fungsi print() di Python
# Instruktur: Thoriq Azis | File: latihan_1_print.py
# ==========================================================

print("=== 1. CETAK TEKS DASAR ===")
print("Halo Dunia! Selamat datang di Lab Komputer SMK.")
print('Pemrograman Python itu mudah, seru, dan menyenangkan!')

print("\\n=== 2. CETAK ANGKA DAN OPERASI HITUNGAN ===")
print(100)
print(50 + 25)

print("\\n=== 3. CETAK BEBERAPA DATA SEKALIGUS ===")
# Menggabungkan teks dan angka menggunakan koma (otomatis diberi spasi)
print("Nama Siswa:", "Thoriq Azis", "| Umur:", 17, "Tahun")

print("\\n=== 4. KARAKTER KHUSUS (\\n untuk Baris Baru, \\t untuk Tab) ===")
print("Daftar Jurusan Unggulan SMK:\\n\\t1. Rekayasa Perangkat Lunak (RPL)\\n\\t2. Teknik Komputer & Jaringan (TKJ)\\n\\t3. Sistem Informasi, Jaringan & Aplikasi (SIJA)")

print("\\n=== 5. TEKNIK MODERN F-STRING (FORMATTED STRING) ===")
sekolah = "SMK Cahaya Pertiwi"
angkatan = 2026
print(f"Saya adalah siswa berprestasi di {sekolah} Angkatan {angkatan}!")
```

---

#### 💻 Panduan Langkah demi Langkah Menjalankan di VS Code:
1. **Buka VS Code** di komputer Anda.
2. Buat file baru bernama **`latihan_1_print.py`** (**File -> New File** lalu simpan).
3. Salin (*copy*) kode di atas lalu tempel (*paste*) ke dalam file tersebut (**Ctrl + S** untuk simpan).
4. Buka Terminal terintegrasi di VS Code (**`Ctrl + \``**).
5. Ketik perintah:
   ```bash
   python latihan_1_print.py
   ```
6. Amati pesan yang muncul di terminal Anda!

---

#### 🎯 Tantangan Praktik Mandiri:
Buatlah tampilan **Kartu Biodata Siswa** sederhana menggunakan `print()`, berisi:
- Nama Lengkap, NISN, Kelas & Jurusan, dan Cita-cita!
*Petunjuk: Gunakan garis pembatas bintang (`print("*" * 40)`).*
"""

    # 2. Topik 2: Variabel dan Tipe Data
    elif any(k in msg_lower for k in ["variabel", "variable", "tipe data", "tipe_data", "datatype", "integer", "string", "float", "boolean", "materi 2", "dasar 2"]) or clean_msg in ["2", "materi 2", "modul 2"]:
        result_text = """### 🏷️ Materi Dasar 2: Variabel dan Tipe Data di Python

Halo sobat siswa SMK! Dalam pemrograman, kita membutuhkan tempat untuk menyimpan data. Inilah peran **Variabel** dan **Tipe Data**.
*Analogi: Variabel itu seperti toples berlabel di dapur. Toples berlabel "Gula" diisi butiran gula, toples berlabel "Minyak" diisi cairan. Label adalah nama variabel, isinya adalah data.*

#### 💡 4 Tipe Data Paling Dasar di Python:
1. **String (`str`)**: Teks atau karakter (harus pakai tanda kutip, contoh: `"SMK Bisa"`).
2. **Integer (`int`)**: Bilangan bulat positif atau negatif (contoh: `17`, `100`, `-5`).
3. **Float (`float`)**: Bilangan desimal/pecahan bertanda titik (contoh: `87.5`, `3.14`).
4. **Boolean (`bool`)**: Hanya memiliki dua nilai kebenaran: `True` (Benar) atau `False` (Salah).

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_2_variabel.py`)
```python
# ==========================================================
# Materi 2: Variabel & Tipe Data Dasar
# Instruktur: Thoriq Azis | File: latihan_2_variabel.py
# ==========================================================

print("=== 1. DEKLARASI VARIABEL DENGAN BERBAGAI TIPE DATA ===")
nama_siswa = "Muhammad Fajar"     # Tipe data: str (String)
nisn = "0058291024"              # Tipe data: str (NISN tidak dihitung matematika)
umur = 16                        # Tipe data: int (Integer)
tinggi_badan = 168.5             # Tipe data: float (Desimal)
sudah_ujian = True               # Tipe data: bool (Boolean)

# Menampilkan data
print(f"Nama Siswa   : {nama_siswa}")
print(f"NISN         : {nisn}")
print(f"Umur         : {umur} Tahun")
print(f"Tinggi Badan : {tinggi_badan} cm")
print(f"Status Ujian : {sudah_ujian}")

print("\\n=== 2. MEMERIKSA TIPE DATA DENGAN FUNGSI type() ===")
print("Tipe nama_siswa    :", type(nama_siswa))
print("Tipe umur          :", type(umur))
print("Tipe tinggi_badan  :", type(tinggi_badan))
print("Tipe sudah_ujian   :", type(sudah_ujian))

print("\\n=== 3. KONVERSI TIPE DATA (TYPE CASTING) ===")
skor_teori = "85"
skor_praktik = "90"
# Konversi ke int dengan int():
total_nilai = int(skor_teori) + int(skor_praktik)
rata_rata = total_nilai / 2
print(f"Total Nilai Benar (Integer) : {total_nilai}")
print(f"Rata-rata Nilai (Float)     : {rata_rata}")
```

---

#### 💻 Panduan Menjalankan di VS Code:
1. Buat file baru di VS Code bernama **`latihan_2_variabel.py`**.
2. Salin kode di atas, tempel, dan simpan (**Ctrl + S**).
3. Buka Terminal VS Code (**Ctrl + \``**), lalu jalankan:
   ```bash
   python latihan_2_variabel.py
   ```

---

#### 🎯 Tantangan Praktik Mandiri:
Buatlah skrip untuk menghitung luas dan keliling persegi panjang:
- Buat variabel `panjang = 20` dan `lebar = 10`.
- Hitung `luas = panjang * lebar` dan `keliling = 2 * (panjang + lebar)`.
- Cetak hasilnya dengan f-string yang rapi!
"""

    # 3. Topik 3: Menerima Inputan Pengguna (input()) & Operasi Aritmatika
    elif any(k in msg_lower for k in ["inputan", "input", "masukan", "user input", "pengguna", "aritmatika", "matematika", "materi 3", "dasar 3"]) or clean_msg in ["3", "materi 3", "modul 3"]:
        result_text = """### ⌨️ Materi Dasar 3: Menerima Inputan Pengguna (`input()`) & Operasi Aritmatika

Halo sobat siswa SMK! Program komputer yang hebat adalah program yang interaktif — dapat menerima masukan langsung dari pengguna keyboard.
*Analogi: Seperti mesin ATM atau kasir supermarket. Layar bertanya "Berapa nominal transaksi?", kita mengetik nominalnya, dan mesin memprosesnya.*

#### 💡 Kunci Utama Fungsi `input()`:
1. Fungsi `input("Pesan: ")` **selalu menghasilkan teks/string (`str`)**, meskipun pengguna mengetik angka!
2. Jika input berupa angka untuk perhitungan, kita **wajib membungkusnya** dengan `int(input(...))` untuk bilangan bulat atau `float(input(...))` untuk bilangan desimal.
3. **Operator Matematika di Python:**
   - `+` (Penjumlahan) | `-` (Pengurangan) | `*` (Perkalian)
   - `/` (Pembagian desimal) | `//` (Pembagian bulat) | `%` (Modulus / Sisa Bagi) | `**` (Pangkat)

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_3_input.py`)
```python
# ==========================================================
# Materi 3: Input Pengguna & Kasir Mini Koperasi SMK
# Instruktur: Thoriq Azis | File: latihan_3_input.py
# ==========================================================

print("==================================================")
print("     SISTEM KASIR KOPERASI SISWA SMK PERTIWI      ")
print("==================================================")

# 1. Mengambil input teks (nama pembeli & nama barang)
nama_siswa = input("Nama Siswa Pembeli : ")
nama_barang = input("Nama Barang Belanja: ")

# 2. Mengambil input angka -> wajib dibungkus int() / float()
harga_satuan = float(input("Harga Satuan Barang (Rp) : "))
jumlah_beli = int(input("Jumlah Barang yang Dibeli: "))

# 3. Operasi Perhitungan Matematika
subtotal = harga_satuan * jumlah_beli
diskon = subtotal * 0.10  # Diskon 10% kartu pelajar
total_bayar = subtotal - diskon

# 4. Menampilkan Struk Pembayaran
print("\\n---------------- STRUK PEMBAYARAN ----------------")
print(f"Pelanggan         : {nama_siswa}")
print(f"Barang Dibeli     : {nama_barang}")
print(f"Harga @ Satuan    : Rp {harga_satuan:,.0f}")
print(f"Kuantitas         : {jumlah_beli} pcs")
print(f"Subtotal          : Rp {subtotal:,.0f}")
print(f"Diskon Pelajar 10%: Rp {diskon:,.0f}")
print("--------------------------------------------------")
print(f"TOTAL HARUS BAYAR : Rp {total_bayar:,.0f}")
print("==================================================")
```

---

#### 💻 Panduan Praktik di VS Code:
1. Buat file baru bernama **`latihan_3_input.py`** di VS Code.
2. Salin kode di atas, tempel, dan simpan (**Ctrl + S**).
3. Buka Terminal di VS Code (**Ctrl + \``**), lalu jalankan:
   ```bash
   python latihan_3_input.py
   ```
4. Ketik nama, harga, dan jumlah di terminal lalu tekan **Enter**!

---

#### 🎯 Tantangan Praktik Mandiri:
Buatlah program **Penghitung Umur Otomatis**:
- Minta input `nama` dan `tahun_lahir` siswa.
- Hitung umur siswa di tahun ini (`2026 - tahun_lahir`).
- Tampilkan sapaan dan umur siswa ke layar!
"""

    # 4. Topik 4: Percabangan (If - Else)
    elif any(k in msg_lower for k in ["if", "percabangan", "kondisi", "else", "elif", "materi 4", "dasar 4"]) or clean_msg in ["4", "materi 4", "modul 4"]:
        result_text = """### 🔀 Materi Dasar 4: Percabangan Kondisi (`if - elif - else`) di Python

Halo sobat SMK! **Percabangan** adalah cara kita mengajarkan komputer untuk mengambil keputusan logis berdasarkan kondisi tertentu.
*Analogi: Jika lampu lalu lintas HIJAU, jalan. Jika KUNING, hati-hati. Jika MERAH, berhenti!*

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_kondisi.py`)
```python
# ==========================================================
# Materi 4: Evaluasi Standar Kelulusan KKM Nilai SMK
# Instruktur: Thoriq Azis | File: latihan_kondisi.py
# ==========================================================

print("=== SISTEM PENENTU PREDIKAT KELULUSAN SISWA SMK ===")

nama_siswa = input("Masukkan Nama Siswa: ")
nilai_kejuruan = float(input("Masukkan Nilai Ujian Praktik (0 - 100): "))

# Standar KKM Sekolah adalah 75.0
kkm = 75.0

# Logika Percabangan If - Elif - Else
if nilai_kejuruan >= 90:
    predikat = "A (Sangat Kompeten / Luar Biasa)"
    status = "LULUS DENGAN PUJIAN"
elif nilai_kejuruan >= kkm:
    predikat = "B (Kompeten)"
    status = "LULUS STANDAR KKM"
elif nilai_kejuruan >= 60:
    predikat = "C (Cukup)"
    status = "REMEDIAL RINGAN"
else:
    predikat = "D (Belum Kompeten)"
    status = "REMEDIAL TOTAL BERSAMA GURU PEMBIMBING"

print("\\n---------------- HASIL EVALUASI ----------------")
print(f"Nama Siswa   : {nama_siswa}")
print(f"Nilai Siswa  : {nilai_kejuruan}")
print(f"Standar KKM  : {kkm}")
print(f"Predikat     : {predikat}")
print(f"Status Akhir : {status}")
```

---

#### 💻 Panduan Menjalankan di VS Code:
1. Buat file baru di VS Code dengan nama **`latihan_kondisi.py`**.
2. Tempel kode di atas lalu simpan (**Ctrl + S**).
3. Jalankan di Terminal VS Code (**Ctrl + \``**):
   ```bash
   python latihan_kondisi.py
   ```

---

#### 🎯 Tantangan Praktik Mandiri:
Tambahkan kondisi jika nilai di atas 100 atau di bawah 0, program akan menampilkan pesan: *"Input tidak valid! Nilai harus antara 0 - 100."*
"""

    # 5. Topik 5: Looping / Perulangan (For & While)
    elif any(k in msg_lower for k in ["loop", "perulangan", "for ", "while", "materi 5", "dasar 5"]) or clean_msg in ["5", "materi 5", "modul 5"]:
        result_text = """### 🔄 Materi Dasar 5: Perulangan (Looping) di Python

Halo sobat siswa SMK! Bersama mentor **Thoriq Azis**, mari kita pelajari konsep **Looping (Perulangan)**.
*Analogi: Seperti lari keliling lapangan upacara sebanyak 5 putaran. Kamu menghitung putaran ke-1, ke-2, sampai ke-5 lalu berhenti.*

Di Python ada 2 jenis looping utama:
1. **`for loop`**: Digunakan jika jumlah putaran sudah diketahui pasti (menggunakan `range()`).
2. **`while loop`**: Digunakan jika perulangan berjalan selama kondisi masih `True`.

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_looping.py`)
```python
# ==========================================================
# Materi 5: Latihan Looping Python
# Instruktur: Thoriq Azis | File: latihan_looping.py
# ==========================================================

print("=== 1. CONTOH FOR LOOP DENGAN range() ===")
# range(1, 6) menghasilkan angka 1, 2, 3, 4, 5
for putaran in range(1, 6):
    print(f"Siswa sedang lari putaran ke-{putaran}")

print("\\n=== 2. CONTOH FOR LOOP MELALUI DAFTAR JURUSAN ===")
jurusan_smk = ["RPL", "TKJ", "SIJA", "Multimedia"]
for nama in jurusan_smk:
    print(f"Jurusan Pilihan: {nama}")

print("\\n=== 3. CONTOH WHILE LOOP (HITUNG MUNDUR ROKET) ===")
hitungan = 5
while hitungan > 0:
    print(f"Peluncuran dalam: {hitungan}...")
    hitungan -= 1  # kurangi 1 setiap putaran

print("ROKET MELUNCUR KE LUAR ANGKASA! 🚀")
```

---

#### 💻 Panduan Menjalankan di VS Code:
1. Simpan kode sebagai **`latihan_looping.py`**.
2. Jalankan perintah di terminal VS Code:
   ```bash
   python latihan_looping.py
   ```

---

#### 🎯 Tantangan Praktik Mandiri:
Modifikasi kode di atas agar:
1. Menampilkan deret bilangan genap dari **2 sampai 20** menggunakan `for loop`! (*Petunjuk: gunakan `range(2, 21, 2)`*).
2. Buat daftar 5 nama teman sekelasmu di dalam list, lalu tampilkan sapaan *"Halo [Nama Teman]!"* menggunakan perulangan!
"""

    # 6. Topik 6: Struktur Data (List & Dictionary)
    elif any(k in msg_lower for k in ["list", "dict", "array", "struktur data", "tuple", "materi 6", "dasar 6"]) or clean_msg in ["6", "materi 6", "modul 6"]:
        result_text = """### 📑 Materi Dasar 6: Struktur Data (List & Dictionary) di Python

Halo sobat SMK! **List** dan **Dictionary** adalah wadah untuk menyimpan banyak data sekaligus dalam satu variabel:
- **`List [ ]`**: Menyimpan daftar berurutan (misal: daftar nama teman sekelas).
- **`Dictionary { }`**: Menyimpan pasangan Kunci & Nilai (*Key: Value*, misal: identitas lengkap siswa).

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_data.py`)
```python
# ==========================================================
# Materi 6: Manajemen Data Siswa Kelas SMK
# Instruktur: Thoriq Azis | File: latihan_data.py
# ==========================================================

# 1. List (Daftar Berurutan)
mata_pelajaran = ["Pemrograman Dasar", "Basis Data", "PBO", "Machine Learning"]
print("Daftar Mapel Awal:", mata_pelajaran)
mata_pelajaran.append("Cloud Computing")  # Menambah data baru
print("Setelah Ditambah :", mata_pelajaran)

# 2. Dictionary (Data Terstruktur Key-Value)
profil_siswa = {
    "nisn": "0051234567",
    "nama": "Ahmad Fadhil",
    "kelas": "XII RPL 1",
    "jurusan": "Rekayasa Perangkat Lokan",
    "nilai": [88, 92, 85, 90]
}

print(f"\\nNama Siswa : {profil_siswa['nama']}")
print(f"Kelas      : {profil_siswa['kelas']}")

# Menghitung rata-rata nilai dari list di dalam dictionary
rata_rata = sum(profil_siswa['nilai']) / len(profil_siswa['nilai'])
print(f"Rata-rata Nilai Siswa: {rata_rata:.1f}")
```

---

#### 💻 Panduan Menjalankan di VS Code:
Simpan sebagai **`latihan_data.py`** lalu jalankan:
```bash
python latihan_data.py
```
"""

    # 7. Topik 7: Membuat Fungsi (def)
    elif any(k in msg_lower for k in ["fungsi", "def ", "function", "parameter", "return", "materi 7", "dasar 7"]) or clean_msg in ["7", "materi 7", "modul 7"]:
        result_text = """### 📦 Materi Dasar 7: Membuat Fungsi (`def`) di Python

Halo sobat SMK! **Fungsi (Function)** adalah blok kode terstruktur yang kita beri nama agar bisa dipanggil berulang kali tanpa mengetik ulang rumusnya.
*Analogi: Seperti tombol blender atau cetakan kue. Cukup buat cetakannya sekali, kita bisa mencetak kue berkali-kali!*

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_fungsi.py`)
```python
# ==========================================================
# Materi 7: Membuat Fungsi Matematika & Kasir SMK
# Instruktur: Thoriq Azis | File: latihan_fungsi.py
# ==========================================================

# 1. Fungsi sederhana tanpa parameter
def sapa_lab():
    print("==========================================")
    print("   SELAMAT DATANG DI LAB KOMPUTER SMK     ")
    print("==========================================")

# 2. Fungsi dengan parameter dan mengembalikan nilai (return)
def hitung_diskon(total_belanja, persen_diskon=10):
    \"\"\"Menghitung potongan harga khusus kartu pelajar SMK\"\"\"
    potongan = total_belanja * (persen_diskon / 100)
    total_akhir = total_belanja - potongan
    return total_akhir, potongan

# Program Utama
sapa_lab()
belanja = 150000
bayar, hemat = hitung_diskon(belanja, 15)

print(f"Total Belanja Awal   : Rp {belanja:,}")
print(f"Hemat Diskon Pelajar : Rp {hemat:,.0f}")
print(f"Total Harus Dibayar  : Rp {bayar:,.0f}")
```

---

#### 💻 Panduan Menjalankan di VS Code:
Simpan sebagai **`latihan_fungsi.py`** dan jalankan:
```bash
python latihan_fungsi.py
```
"""

    # 8. Topik 8: Penanganan Error (Try - Except)
    elif any(k in msg_lower for k in ["error", "try", "except", "penanganan error", "exception", "crash", "materi 8", "dasar 8"]) or clean_msg in ["8", "materi 8", "modul 8"]:
        result_text = """### 🛡️ Materi Dasar 8: Penanganan Error (`try - except`) di Python

Halo sobat SMK! Pernahkah programmu tiba-tiba keluar dan berhenti dengan tulisan merah panjang saat salah mengetik angka? Itu namanya **Crash / Unhandled Exception**.
*Analogi: Seperti helm pengaman saat naik motor. `try-except` melindungi program agar tidak berhenti mendadak saat terjadi kesalahan input.*

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_8_error.py`)
```python
# ==========================================================
# Materi 8: Penanganan Error Input Pengguna
# Instruktur: Thoriq Azis | File: latihan_8_error.py
# ==========================================================

print("=== PROGRAM PEMBAGIAN AMAN (ANTI CRASH) ===")

try:
    angka_1 = float(input("Masukkan angka pertama : "))
    angka_2 = float(input("Masukkan angka pembagi : "))
    
    hasil = angka_1 / angka_2
    print(f"Hasil Pembagian: {hasil}")

except ValueError:
    print("⚠️ Kesalahan: Input harus berupa angka, bukan huruf atau simbol!")

except ZeroDivisionError:
    print("⚠️ Kesalahan: Angka tidak dapat dibagi dengan angka nol (0)!")

finally:
    print("Program selesai dijalankan dengan aman.")
```

---

#### 💻 Panduan Menjalankan di VS Code:
Simpan sebagai **`latihan_8_error.py`** dan jalankan:
```bash
python latihan_8_error.py
```
*Cobalah sengaja mengetik huruf seperti "abc" saat diminta angka, dan lihat bagaimana program menangkap error secara anggun tanpa crash!*
"""

    # 9. Topik 9: Machine Learning Pertama di VS Code (Mudah Dipahami Siswa SMK)
    elif any(k in msg_lower for k in [
        "machine learning", "ml", "ai", "model", "prediksi", "klasifikasi", "regresi",
        "overfitting", "akurasi", "confusion matrix", "feature importance",
        "materi 9", "dasar 9", "apa itu ml", "kenapa ml susah"
    ]) or clean_msg in ["9", "materi 9", "modul 9", "ml", "machine learning"]:
        result_text = f"""### 🤖 Materi 9: Machine Learning Sederhana & Ramah untuk Siswa SMK

Halo sobat SMK! Jangan khawatir, **Machine Learning (ML)** sebenarnya **tidak seseram rumus matematika yang rumit**. 
Bersama mentor **Thoriq Azis, S.Kom**, mari kita pahami logika dasarnya dengan perumpamaan dunia nyata!

---

#### 💡 Apa Sih Bedanya Coding Biasa dengan Machine Learning?
- **Coding Biasa (Traditional Programming)**: Kita sebagai programmer harus mengetik aturan logika satu per satu (`if umur < 18 and tiket == 1: selamat = True`). Kalau datanya ada ribuan jenis, kita pasti pusing menulis ribuan `if-else`.
- **Machine Learning**: Kita cukup memberikan **ribuan data masa lalu lengkap dengan kunci jawabannya** ke komputer. Komputer akan membaca dan **menemukan polanya sendiri secara otomatis**!

---

#### 🎒 Kamus Gaul 6 Istilah Penting Machine Learning:
1. **Dataset**: Buku kumpulan soal latihan masa lalu (misal: data 891 penumpang Titanic).
2. **Fitur (Feature / X)**: Petunjuk atau ciri-ciri soal (misal: Umur, Jenis Kelamin, Harga Tiket, Kelas Kabin).
3. **Target (Label / y)**: Kunci jawaban yang ingin ditebak komputer (misal: Selamat / Tidak Selamat).
4. **Data Latih (Train 80%)**: Masa belajar komputer dengan kunci jawaban terbuka untuk mengenali pola.
5. **Data Uji (Test 20%)**: Ujian tertutup! Komputer diuji menebak 20% data yang belum pernah dilihat tanpa boleh mencontek.
6. **Akurasi (Nilai Ulangan)**: Berapa persen tebakan komputer yang tepat sasaran saat ujian.
7. **Overfitting ("Hafal Mati")**: Penyakit model yang cuma menghafal kunci jawaban latihan, tapi begitu diberi soal ujian baru nilainya langsung remedial!

---

#### 🐍 Skrip Python Praktik Mandiri di VS Code (`proyek_ml_smk.py`)
Berikut adalah skrip Machine Learning perdana Anda menggunakan dataset aktif **`{dataset_name}`** dengan target **`{target_col}`**:

```python
# ==========================================================
# Praktikum Machine Learning Siswa SMK Cahaya Pertiwi
# Instruktur: Thoriq Azis | File: proyek_ml_smk.py
# ==========================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=== 1. MEMBUKA BUKU SOAL (DATASET) ===")
# Memuat data
df = pd.read_csv("{dataset_name}.csv")
target = "{target_col}"

# Memilih fitur angka (X) dan kunci jawaban (y)
X = df.drop(columns=[target]).select_dtypes(include=['number']).fillna(0)
y = df[target]
print(f"Total Soal Latihan: {{len(df)}} baris data.")

print("\\n=== 2. MEMBAGI MASA BELAJAR (80%) & UJIAN (20%) ===")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data Belajar (Train): {{len(X_train)}} siswa")
print(f"Data Ujian   (Test) : {{len(X_test)}} siswa")

print("\\n=== 3. KOMPUTER MULAI BELAJAR POLA (TRAINING) ===")
# Menggunakan Random Forest (Musyawarah 100 Siswa Pintar)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("✓ Komputer selesai mempelajari pola data!")

print("\\n=== 4. UJIAN TERTUTUP & MENGHITUNG NILAI RAPOR (TESTING) ===")
tebakan = model.predict(X_test)
nilai_rapor = accuracy_score(y_test, tebakan) * 100

print("=" * 55)
print(f"🎯 NILAI RAPOR KELULUSAN MODEL: {{nilai_rapor:.2f}} / 100")
if nilai_rapor >= 80:
    print("🏆 Predikat: Sangat Cerdas (Grade A) - Siap Dipakai!")
else:
    print("👍 Predikat: Lulus Ujian Dasar (Grade B) - Cukup Bagus!")
print("=" * 55)
```

---

#### 💻 Cara Menjalankannya di VS Code:
1. Pastikan pustaka AI terinstal di terminal VS Code (**Ctrl + `**):
   ```bash
   pip install pandas scikit-learn
   ```
2. Jalankan skrip:
   ```bash
   python proyek_ml_smk.py
   ```

---

#### 🎯 Tantangan Praktik Mandiri:
1. Coba ubah `n_estimators=100` menjadi `200` atau `50` pada baris 33, lalu amati apakah nilai akurasi ujiannya berubah naik atau turun!
2. Buka tab **"Coba Langsung (AutoML)"** di studio ini untuk melihat komputer menguji 5 algoritma AI sekaligus secara otomatis!
"""

    elif any(k in msg_lower for k in [
        "titanic", "iris", "bedah dataset", "dataset contoh", "dataset standar",
        "pilihan dataset", "kenapa dataset", "mengapa dataset", "alasan dataset",
        "kenapa harus titanic", "kenapa data", "6 dataset"
    ]) or "titanic" in msg_lower or "iris" in msg_lower or (
        "dataset" in msg_lower and any(w in msg_lower for w in ["kenapa", "mengapa", "alasan", "apa", "pilih", "contoh", "bedah", "6", "enam"])
    ) or clean_msg in ["dataset", "datasets", "titanic", "kenapa titanic", "kenapa harus titanic"]:
        result_text = """### 📊 Bedah 6 Dataset Standar Dunia: Mengapa Harus Titanic, Iris, & Gaji?

Halo sobat siswa SMK! Bersama mentor **Thoriq Azis, S.Kom**, mari kita bedah alasan ilmiah mengapa 6 dataset ini menjadi **standar emas internasional** dalam kurikulum Machine Learning dunia:

---

#### 🚢 1. Titanic Survival (Klasifikasi Biner)
- **Kisah Nyata 1912**: Tragedi tenggelamnya kapal Titanic dengan jumlah sekoci penyelamat terbatas.
- **Mengapa Harus Dipelajari Siswa?**:
  1. **Logika Manusiawi**: Aturan evakuasi memprioritaskan wanita & anak-anak (*"women and children first"*), serta penumpang kelas kabin 1 (orang kaya). Siswa dapat membuktikan apakah AI mampu mendeteksi pola penyelamatan ini!
  2. **Tantangan Data Riil (*Data Cleaning*)**: Di dunia nyata, data tidak pernah sempurna. Titanic melatih siswa mengisi data umur yang hilang (*missing values*) dan mengubah data teks (Pria/Wanita) menjadi angka (*encoding*).
  3. **Target Prediksi**: Biner (Selamat = 1, Meninggal = 0).

---

#### 🌸 2. Iris Flower (Klasifikasi Multi-Kelas Tertua Dunia)
- **Sejarah 1936**: Dibuat oleh Ronald Fisher tahun 1936, ini adalah *dataset tertua dan paling dihormati* di dunia Machine Learning!
- **Mengapa Harus Dipelajari Siswa?**:
  1. **Tebak 3 Spesies Bunga**: Melatih AI membedakan 3 spesies bunga iris (*Setosa*, *Versicolor*, dan *Virginica*).
  2. **Data Sangat Bersih**: Tepat 150 baris data tanpa ada nilai kosong, sangat cocok sebagai langkah awal sebelum data yang rumit.
  3. **Fitur Fisik**: Menggunakan panjang & lebar mahkota serta kelopak daun.

---

#### 💼 3. Prediksi Gaji & Pengalaman Kerja (Regresi Linier)
- **Relevan dengan Siswa SMK**: Menaksir perkiraan gaji bulanan berdasarkan lama tahun pengalaman kerja di industri.
- **Mengapa Harus Dipelajari Siswa?**:
  1. **Memahami Regresi**: Yang ditebak komputer bukan label kategori kata, melainkan **angka nominal uang rupiah nyata**.
  2. **Pola Hubungan Lurus (*Linear Relationship*)**: Sangat intuitif bagi pemula—semakin bertambah pengalaman, semakin tinggi ekspektasi gajinya.

---

#### 👥 4. Customer Churn (Kasus Bisnis Nyata & Industri)
- **Dunia Telekomunikasi & Layanan**: Mengetahui apakah pelanggan Telkomsel / Netflix berniat berhenti berlangganan (*churn*).
- **Mengapa Harus Dipelajari Siswa?**:
  1. **Nilai Bisnis Tinggi**: Perusahaan rela berinvestasi AI demi mendeteksi pelanggan yang kecewa sebelum mereka pindah ke kompetitor.
  2. **Fitur Kompleks**: Melibatkan jenis kontrak (bulanan/tahunan), tagihan, dan riwayat komplain.

---

#### 🏡 5. Prediksi Harga Rumah (Regresi Multi-Variabel)
- **Dunia Properti**: Menaksir harga jual pasar wajar suatu properti/rumah.
- **Mengapa Harus Dipelajari Siswa?**:
  1. **Banyak Faktor Penentu**: Harga properti ditentukan kombinasi luas tanah, jumlah kamar tidur, dan lokasi.
  2. **Feature Importance**: Siswa belajar melihat fitur mana yang paling mendongkrak harga rumah secara signifikan.

---

#### 🩺 6. Skrining Diabetes (Healthcare AI & Medis)
- **Pemanfaatan AI untuk Kemanusiaan**: Membantu rumah sakit mendeteksi dini apakah seorang pasien berisiko tinggi mengidap diabetes.
- **Mengapa Harus Dipelajari Siswa?**:
  1. **Data Medis Klinis**: Melibatkan kadar glukosa darah, tekanan darah, indeks massa tubuh (BMI), dan usia pasien.
  2. **Pentingnya Akurasi**: Di bidang kesehatan, salah prediksi (*False Negative*) sangat berbahaya bagi pasien.

---

#### 🗺️ Urutan Belajar yang Disarankan (Roadmap):
1. **Langkah 1**: 🚢 *Titanic* (Logika 2 pilihan & pembersihan data).
2. **Langkah 2**: 💼 *Prediksi Gaji* (Menebak nominal angka uang / Regresi).
3. **Langkah 3**: 🌸 *Iris Flower* (Klasifikasi 3 jenis kelompok bunga).
4. **Langkah 4**: 👥 *Customer Churn* & 🩺 *Diabetes* (Studi kasus nyata industri & kesehatan).

---

💡 **Kabar Baik!** Materi penjelasan lengkap ini beserta **tombol ⚡ Uji Coba Langsung di Studio ML** untuk masing-masing dataset sudah disematkan langsung di dalam **Menu E-Learning & Ujian** (pada bagian *Materi Pembelajaran: Mengapa Harus Data Titanic, Iris, & Gaji?*). Anda bisa langsung mencoba datasetnya dalam 1 klik!"""

    # 10. Topik 10: PRD / Jobsheet Praktikum Siswa SMK
    elif any(k in msg_lower for k in ["prd", "jobsheet", "lembar kerja", "materi 10", "dasar 10"]) or clean_msg in ["10", "materi 10", "modul 10"]:
        result_text = generate_local_prd(f"Praktikum Python & ML: Prediksi {target_col}", dataset_name, task_type, target_col)

    # 11. Topik 11: Basis Data & Query SQL (Database Relasional SQLite di Python)
    elif any(k in msg_lower for k in [
        "database", "basis data", "basis_data", "sql", "sqlite", "mysql", "mariadb", 
        "postgresql", "postgres", "query", "tabel", "table", "rdbms", "select", 
        "insert", "update", "delete", "crud", "join", "where", "primary key", 
        "foreign key", "materi 11", "dasar 11", "materi database", "materi sql"
    ]) or clean_msg in ["11", "materi 11", "modul 11", "database", "sql", "mysql", "sqlite", "query"]:
        result_text = """### 🗄️ Materi 11: Basis Data & Query SQL (Database Relasional SQLite & MySQL di Python)

Halo sobat siswa SMK! Dalam dunia industri teknologi modern, web backend, dan Machine Learning, program komputer membutuhkan tempat penyimpanan data yang permanen, terstruktur, dan aman. Inilah peran utama **Basis Data Relasional (Database SQL)**.
*Analogi: Bayangkan lemari arsip digital di SMK Cahaya Pertiwi. Lemari itu adalah **Database**, setiap laci adalah **Tabel** (misal tabel `siswa` dan tabel `nilai_mapel`), setiap map dokumen di dalam laci adalah **Baris Data (Record)**, dan kolom formulirnya adalah **Field/Kolom (NISN, Nama, Jurusan)**.*

---

#### 💡 Konsep Penting Database & SQL:
1. **RDBMS (*Relational Database Management System*)**: Sistem manajemen data berbasis tabel-tabel yang saling terhubung (berelasi).
2. **SQLite vs MySQL di Dunia Nyata:**
   - **SQLite**: Database file lokal tanpa server (*serverless*). Sangat istimewa karena **sudah terpasang bawaan di Python (`import sqlite3`)** tanpa perlu instalasi aplikasi server seperti XAMPP atau MySQL Server!
   - **MySQL / MariaDB**: Database berbasis client-server yang biasa digunakan untuk aplikasi web skala besar. Di Python dihubungkan menggunakan library `mysql-connector-python` atau `pymysql`.
   - **Kunci Utama**: Sintaks query SQL dasar (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`, `INNER JOIN`) adalah **99% IDENTIK** pada MySQL dan SQLite karena keduanya mematuhi standar internasional ANSI SQL! Apa yang Anda pelajari di sini langsung bisa Anda pakai di MySQL!
3. **Operasi Inti CRUD & SQL Fundamental:**
   - `CREATE TABLE`: Menyiapkan struktur tabel, nama kolom, dan tipe data (`INTEGER`, `TEXT`, `REAL`).
   - `PRIMARY KEY`: Kolom identitas unik untuk setiap baris data (contoh: ID atau NISN).
   - `INSERT INTO`: Menambahkan data rekaman baru ke tabel.
   - `SELECT ... WHERE ... ORDER BY`: Mengambil data, menyaring kriteria tertentu, dan mengurutkan.
   - `INNER JOIN`: Menghubungkan data dari dua tabel berbeda berdasarkan kunci relasi (*Foreign Key*).
   - `UPDATE ... SET`: Memperbarui data yang sudah tersimpan.
   - `DELETE FROM`: Menghapus baris data.

---

#### 🐍 Skrip Kode Python Lengkap (`latihan_11_database_sqlite.py`)
Salin kode praktikum database relasional di bawah ini:

```python
# ==========================================================
# Materi 11: Basis Data & Query SQL Menggunakan SQLite di Python
# Instruktur: Thoriq Azis | File: latihan_11_database_sqlite.py
# ==========================================================

import sqlite3

print(">>> [Langkah 1] Menghubungkan ke database SQLite (sekolah_smk.db)...")
# File database otomatis dibuat jika belum ada di folder proyek
conn = sqlite3.connect("sekolah_smk.db")
cursor = conn.cursor()

print(">>> [Langkah 2] Membuat tabel 'siswa' dan 'nilai_mapel'...")
# 1. Tabel Siswa
cursor.execute('''
CREATE TABLE IF NOT EXISTS siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nisn TEXT UNIQUE NOT NULL,
    nama TEXT NOT NULL,
    kelas TEXT NOT NULL,
    jurusan TEXT NOT NULL
);
''')

# 2. Tabel Nilai Mapel (Berelasi dengan tabel siswa melalui siswa_id)
cursor.execute('''
CREATE TABLE IF NOT EXISTS nilai_mapel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    siswa_id INTEGER,
    mapel TEXT NOT NULL,
    nilai REAL NOT NULL,
    FOREIGN KEY (siswa_id) REFERENCES siswa (id)
);
''')

print(">>> [Langkah 3] Menyisipkan data sampel siswa SMK...")
# Bersihkan data lama untuk latihan
cursor.execute("DELETE FROM nilai_mapel;")
cursor.execute("DELETE FROM siswa;")

# Menambahkan data siswa
data_siswa = [
    ("001", "Ahmad Rizki", "XII RPL 1", "RPL"),
    ("002", "Budi Santoso", "XII RPL 1", "RPL"),
    ("003", "Citra Dewi", "XII TKJ 2", "TKJ"),
    ("004", "Thoriq Azis", "XII RPL 1", "RPL")
]
cursor.executemany("INSERT INTO siswa (nisn, nama, kelas, jurusan) VALUES (?, ?, ?, ?);", data_siswa)

# Menambahkan data nilai kejuruan
data_nilai = [
    (1, "Python Programming", 92.5),
    (1, "Machine Learning", 88.0),
    (2, "Python Programming", 74.0),
    (3, "Jaringan Komputer", 85.0),
    (4, "Python Programming", 98.0),
    (4, "Machine Learning", 96.5)
]
cursor.executemany("INSERT INTO nilai_mapel (siswa_id, mapel, nilai) VALUES (?, ?, ?);", data_nilai)
conn.commit()
print("    ✓ Data berhasil disimpan ke database!")

print("\\n" + "=" * 55)
print(">>> [Langkah 4] Query SELECT Sederhana & Filter WHERE:")
print("    Menampilkan siswa dari jurusan 'RPL':")
print("=" * 55)
cursor.execute("SELECT id, nisn, nama, kelas FROM siswa WHERE jurusan = 'RPL' ORDER BY id ASC;")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r[0]} | NISN: {r[1]} | Nama: {r[2]} | Kelas: {r[3]}")

print("\\n" + "=" * 55)
print(">>> [Langkah 5] Query Relasi Tabel Menggunakan INNER JOIN:")
print("    Menghubungkan data siswa dengan nilai mata pelajaran:")
print("=" * 55)
query_join = '''
SELECT s.nama, s.jurusan, n.mapel, n.nilai
FROM siswa s
INNER JOIN nilai_mapel n ON s.id = n.siswa_id
WHERE n.nilai >= 85.0
ORDER BY n.nilai DESC;
'''
cursor.execute(query_join)
hasil_join = cursor.fetchall()

print(f"{'Nama Siswa':<15} | {'Jurusan':<8} | {'Mata Pelajaran':<20} | {'Nilai':<6}")
print("-" * 55)
for row in hasil_join:
    print(f"{row[0]:<15} | {row[1]:<8} | {row[2]:<20} | {row[3]:<6.1f}")

print("\\n" + "=" * 55)
print(">>> [Langkah 6] Query Agregasi: Menghitung Rata-rata Nilai:")
print("=" * 55)
cursor.execute("SELECT mapel, COUNT(*), AVG(nilai) FROM nilai_mapel GROUP BY mapel;")
for stat in cursor.fetchall():
    print(f"Mapel: {stat[0]:<20} | Jumlah Peserta: {stat[1]} | Rata-rata: {stat[2]:.2f}")

# Menutup koneksi database
conn.close()
print("\\n>>> Praktikum Database SQLite Berhasil Diselesaikan!")
```

---

#### 💻 Panduan Langkah demi Langkah Menjalankan di VS Code:
1. **Buka Visual Studio Code (VS Code)** di komputer Anda.
2. Buat file baru bernama **`latihan_11_database_sqlite.py`** (**File -> New File** lalu simpan dengan **Ctrl + S**).
3. Salin (*copy*) seluruh skrip di atas dan tempel (*paste*) ke dalam editor.
4. Buka Terminal terintegrasi di VS Code (**`Ctrl + \``**).
5. Jalankan perintah:
   ```bash
   python latihan_11_database_sqlite.py
   ```
6. **Periksa File Database**: Di panel Explorer sebelah kiri VS Code, Anda akan melihat file database baru bernama **`sekolah_smk.db`** telah terbuat secara otomatis!
   *(Tips: Anda bisa menginstal ekstensi VS Code bernama "SQLite Viewer" untuk melihat isi tabel database secara visual).*

---

#### 🎯 Tantangan Praktik Mandiri Siswa (Hands-on Challenge):
1. **Tambah Siswa Baru**: Tambahkan 1 siswa baru dengan data Anda sendiri (Nama, NISN, Kelas, Jurusan).
2. **Kueri Nilai Tertinggi**: Buat query `SELECT` untuk mencari siswa yang memperoleh nilai tertinggi pada mapel `"Python Programming"`.
3. **Uji Perintah UPDATE**: Buat perintah `UPDATE nilai_mapel SET nilai = 85.0 WHERE siswa_id = 2;` untuk memberikan nilai remedial siswa, lalu cetak hasilnya kembali!
"""

    # 12. Topik Spesifikasi Teknis / Sprint Task
    elif "task" in msg_lower or "sprint" in msg_lower or "spec" in msg_lower:
        result_text = generate_local_feature_spec(
            feature_name="Praktikum Mandiri Python di VS Code",
            goal="Menyelesaikan latihan pemrograman Python dan mini ML secara bertahap",
            target_user="Siswa SMK & Guru Pembimbing",
            complexity="Medium",
            current_context=current_context
        )

    # Default: Menu Bantuan Kurikulum Berurutan
    else:
        result_text = f"""### 🎓 Halo Sobat SMK! AI Mentor Python & Database Siap Membantu

Saya adalah asisten AI yang siap memandu Anda belajar pemrograman Python dan Basis Data (SQL) secara terstruktur dari dasar hingga mahir untuk langsung dipraktikkan di **Visual Studio Code (VS Code)**!

Berikut urutan materi praktik dasar yang bisa Anda pilih:
- 📢 **Ketik "1" atau "Cetak Teks"**: Fungsi `print()`, escape sequence, dan f-string.
- 🏷️ **Ketik "2" atau "Variabel"**: Tipe data `str`, `int`, `float`, `bool`, dan type casting.
- ⌨️ **Ketik "3" atau "Input"**: Menerima input keyboard dengan `input()` dan operasi aritmatika.
- 🔀 **Ketik "4" atau "Percabangan"**: Logika `if-elif-else` penentu kelulusan nilai SMK.
- 🔄 **Ketik "5" atau "Looping"**: Perulangan `for` dan `while` + tantangan hitung putaran.
- 📑 **Ketik "6" atau "List & Dict"**: Struktur data kumpulan nilai dan profil siswa.
- 📦 **Ketik "7" atau "Fungsi"**: Membuat fungsi `def` modular dengan parameter & return.
- 🛡️ **Ketik "8" atau "Try Except"**: Menangani error agar program tidak crash saat salah input.
- 🤖 **Ketik "9" atau "Machine Learning"**: Skrip Machine Learning perdana di VS Code.
- 📊 **Ketik "Dataset" atau "Titanic"**: Alasan ilmiah pemilihan 6 dataset standar dunia (Titanic, Iris, Gaji, Churn, Rumah, Diabetes).
- 📄 **Ketik "10" atau "Jobsheet PRD"**: Menghasilkan Lembar Kerja Praktikum Siswa siap cetak!
- 🗄️ **Ketik "11" atau "Database"**: Basis data relasional SQLite di Python, tabel, CRUD, dan query JOIN.

*💡 Anda juga bisa langsung mengklik salah satu tombol pintasan materi di atas bar chat!*
"""

    if return_dict:
        return {
            "reply": result_text,
            "provider_used": "local",
            "gemini_error": gemini_error
        }
    return result_text
