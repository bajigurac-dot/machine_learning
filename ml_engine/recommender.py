AVAILABLE_MODELS = {
    "classification": [
        {
            "id": "random_forest",
            "name": "Random Forest Classifier",
            "icon": "🌲",
            "badge": "Paling Populer & Stabil",
            "description": "Ensemble decision tree yang sangat tangguh, tahan overfitting, dan mampu menangkap relasi non-linear yang kompleks.",
            "analogi_smk": "🌲 Musyawarah 100 Siswa Pintar: Seperti mengumpulkan 100 siswa cerdas untuk voting bersama. Keputusan kelompok jauh lebih adil dan minim salah ketimbang pendapat 1 orang.",
            "tips_pemula": "Pilihan paling aman, stabil, dan direkomendasikan untuk hampir semua data!",
            "pros": ["Akurasi konsisten tinggi", "Mampu menangani data campur numerik & kategori", "Menghitung Feature Importance"],
            "params": {
                "n_estimators": {"type": "int", "default": 100, "min": 10, "max": 300, "step": 10, "label": "Jumlah Pohon (Trees)", "smk_hint": "Berapa banyak siswa/pohon yang diajak voting bersama. Default: 100."},
                "max_depth": {"type": "int", "default": 10, "min": 2, "max": 30, "step": 1, "label": "Kedalaman Maksimal", "smk_hint": "Batas level pertanyaan pohon. Jangan terlalu tinggi agar tidak menghafal mati (overfitting)."},
                "random_state": {"type": "int", "default": 42, "min": 0, "max": 999, "step": 1, "label": "Random State", "smk_hint": "Kunci acak agar hasil eksperimen selalu konsisten saat diulang."}
            }
        },
        {
            "id": "gradient_boosting",
            "name": "Gradient Boosting (GBM)",
            "icon": "⚡",
            "badge": "Performa Tinggi",
            "description": "Membangun pohon secara sekuensial untuk mengoreksi kesalahan pohon sebelumnya, seringkali menghasilkan skor akurasi tertinggi.",
            "analogi_smk": "⚡ Belajar dari Remedial: Pohon pertama menebak, pohon kedua fokus memperbaiki salahnya pohon pertama, pohon ketiga menyempurnakan lagi hingga sangat presisi.",
            "tips_pemula": "Sering menjadi andalan juara kompetisi Data Science karena akurasinya sangat tinggi.",
            "pros": ["Presisi sangat tajam", "Optimal untuk kompetisi & dataset terstruktur"],
            "params": {
                "n_estimators": {"type": "int", "default": 100, "min": 20, "max": 250, "step": 10, "label": "Jumlah Estimators", "smk_hint": "Tahapan putaran perbaikan kesalahan."},
                "learning_rate": {"type": "float", "default": 0.1, "min": 0.01, "max": 0.5, "step": 0.01, "label": "Learning Rate", "smk_hint": "Langkah kehati-hatian dalam memperbaiki kesalahan (makin kecil makin hati-hati)."},
                "max_depth": {"type": "int", "default": 4, "min": 1, "max": 10, "step": 1, "label": "Kedalaman Maksimal", "smk_hint": "Ukuran tiap pohon koreksi."}
            }
        },
        {
            "id": "logistic_regression",
            "name": "Logistic Regression",
            "icon": "📈",
            "badge": "Cepat & Mudah Diinterpretasi",
            "description": "Model statistik probabilistik klasik yang sangat cepat, efisien, dan memberikan bobot koefisien yang jelas.",
            "analogi_smk": "📈 Termometer Peluang: Menimbang ciri-ciri untuk mengukur persentase kemungkinan (contoh: 85% Peluang Lulus vs 15% Tidak Lulus).",
            "tips_pemula": "Pelatihannya super kilat dan gampang diubah ke rumus matematika simpel.",
            "pros": ["Kecepatan pelatihan kilat", "Sangat mudah dipahami dan diekspor"],
            "params": {
                "C": {"type": "float", "default": 1.0, "min": 0.01, "max": 10.0, "step": 0.1, "label": "Regulerisasi (C)", "smk_hint": "Tingkat kelenturan garis pemisah peluang."},
                "max_iter": {"type": "int", "default": 200, "min": 50, "max": 1000, "step": 50, "label": "Max Iterations", "smk_hint": "Batas putaran kalkulasi pencarian garis terbaik."}
            }
        },
        {
            "id": "decision_tree",
            "name": "Decision Tree",
            "icon": "🌿",
            "badge": "Transparan / White-box",
            "description": "Pohon keputusan tunggal yang membagi data berdasarkan aturan kondisi if-else yang sangat mudah dibaca manusia.",
            "analogi_smk": "🌿 Bagan Alur Tanya-Jawab: Mirip game tebak-tebakan 20 pertanyaan ('Apakah umur < 18? Jika ya, apakah tiket kelas 1?'). Sangat mudah dibaca alur logikanya!",
            "tips_pemula": "Paling cocok jika guru atau penguji ingin melihat alasan mengapa komputer mengambil keputusan.",
            "pros": ["Penjelasan logika paling gamblang", "Ringan"],
            "params": {
                "max_depth": {"type": "int", "default": 6, "min": 1, "max": 20, "step": 1, "label": "Kedalaman Maksimal", "smk_hint": "Berapa cabang pertanyaan yang boleh diajukan."},
                "min_samples_split": {"type": "int", "default": 2, "min": 2, "max": 20, "step": 1, "label": "Min Sampel Pembagian", "smk_hint": "Minimal jumlah data untuk membuat cabang pertanyaan baru."}
            }
        },
        {
            "id": "knn",
            "name": "K-Nearest Neighbors (KNN)",
            "icon": "📍",
            "badge": "Berbasis Kedekatan",
            "description": "Mengklasifikasikan data berdasarkan mayoritas label dari tetangga terdekat di ruang dimensi data.",
            "analogi_smk": "📍 Prinsip Teman Sebangku: 'Sifatmu mirip dengan 5 teman terdekatmu'. Komputer melihat 5 data tetangga terdekat untuk menentukan tebakan.",
            "tips_pemula": "Sangat alami dan masuk akal untuk data yang berkelompok.",
            "pros": ["Bekerja intuitif untuk data spasial dan klaster"],
            "params": {
                "n_neighbors": {"type": "int", "default": 5, "min": 1, "max": 25, "step": 2, "label": "Jumlah Tetangga (K)", "smk_hint": "Berapa banyak teman terdekat yang diajak voting label."},
                "weights": {"type": "choice", "default": "uniform", "options": ["uniform", "distance"], "label": "Bobot Tetangga", "smk_hint": "Apakah tetangga yang lebih dekat suaranya lebih diutamakan."}
            }
        },
        {
            "id": "svc",
            "name": "Support Vector Classifier (SVM)",
            "icon": "🎯",
            "badge": "Margin Maksimal",
            "description": "Menemukan bidang pemisah (hyperplane) dengan margin terlebar antar kelas dengan kernel RBF.",
            "analogi_smk": "🎯 Pagar Pembatas Terlebar: Memasang pagar pembatas selebar dan seaman mungkin di antara dua kelompok agar tidak tertukar.",
            "tips_pemula": "Bagus saat data memiliki batas perbedaan antar kelas yang tegas.",
            "pros": ["Efektif pada dimensi tinggi", "Kuat pada data dengan batas kelas tajam"],
            "params": {
                "C": {"type": "float", "default": 1.0, "min": 0.1, "max": 10.0, "step": 0.5, "label": "Parameter C", "smk_hint": "Toleransi terhadap data yang sedikit menyeberang pagar."},
                "kernel": {"type": "choice", "default": "rbf", "options": ["rbf", "linear"], "label": "Tipe Kernel", "smk_hint": "Bentuk pagar pembatas (garis lurus atau melengkung)."}
            }
        }
    ],
    "regression": [
        {
            "id": "random_forest_regressor",
            "name": "Random Forest Regressor",
            "icon": "🌲",
            "badge": "Pilihan Utama Regresi",
            "description": "Kumpulan pohon keputusan untuk memprediksi angka kontinu dengan presisi tinggi dan minim risiko overfitting.",
            "analogi_smk": "🌲 Rata-rata Taksiran 100 Ahli: Mengumpulkan taksiran angka/harga dari 100 pohon lalu diambil nilai rata-ratanya.",
            "tips_pemula": "Paling tangguh untuk menebak angka kontinu seperti harga, gaji, atau nilai ujian.",
            "pros": ["Dapat memodelkan kurva rumit", "Tahan outlier"],
            "params": {
                "n_estimators": {"type": "int", "default": 100, "min": 10, "max": 300, "step": 10, "label": "Jumlah Pohon", "smk_hint": "Banyaknya pohon penaksir angka."},
                "max_depth": {"type": "int", "default": 10, "min": 2, "max": 30, "step": 1, "label": "Kedalaman Maksimal", "smk_hint": "Batas kedalaman pertanyaan."},
                "random_state": {"type": "int", "default": 42, "min": 0, "max": 999, "step": 1, "label": "Random State", "smk_hint": "Kunci acak konsistensi."}
            }
        },
        {
            "id": "gradient_boosting_regressor",
            "name": "Gradient Boosting Regressor",
            "icon": "⚡",
            "badge": "Performa Akurasi Tinggi",
            "description": "Mengoptimalkan fungsi loss regresi secara bertahap untuk meminimalkan selisih prediksi (error/MAE/RMSE).",
            "analogi_smk": "⚡ Koreksi Selisih Bertahap: Mengurangi selisih tebakan sedikit demi sedikit sampai tebakan angka mendekati kenyataan.",
            "tips_pemula": "Tingkat melesetnya (error) biasanya paling kecil di antara model regresi lainnya.",
            "pros": ["Error terendah pada dataset terstruktur", "Koreksi residu bertahap"],
            "params": {
                "n_estimators": {"type": "int", "default": 100, "min": 20, "max": 250, "step": 10, "label": "Jumlah Estimators", "smk_hint": "Banyak putaran perbaikan selisih angka."},
                "learning_rate": {"type": "float", "default": 0.1, "min": 0.01, "max": 0.5, "step": 0.01, "label": "Learning Rate", "smk_hint": "Kadar kehati-hatian penyesuaian angka."},
                "max_depth": {"type": "int", "default": 4, "min": 1, "max": 10, "step": 1, "label": "Kedalaman Maksimal", "smk_hint": "Batas level pohon."}
            }
        },
        {
            "id": "linear_regression",
            "name": "Linear Regression",
            "icon": "📏",
            "badge": "Garis Tren Klasik",
            "description": "Menemukan garis lurus tren hubungan terbaik antara fitur input dan variabel target kontinu.",
            "analogi_smk": "📏 Tarikan Garis Penggaris: Menarik garis lurus tren data (contoh: makin banyak jam belajar, makin tinggi perkiraan nilai ujiannya).",
            "tips_pemula": "Paling dasar dan mudah dipahami konsep sebab-akibatnya.",
            "pros": ["Komputasi instan", "Koefisien memiliki arti matematis langsung"],
            "params": {
                "fit_intercept": {"type": "choice", "default": "true", "options": ["true", "false"], "label": "Hitung Intercept", "smk_hint": "Apakah garis tren dimulai dari titik potong dasar."}
            }
        },
        {
            "id": "decision_tree_regressor",
            "name": "Decision Tree Regressor",
            "icon": "🌿",
            "badge": "Mudah Dimengerti",
            "description": "Pohon regresi yang membagi rentang nilai angka menjadi blok-blok keputusan yang mudah dianalisis.",
            "analogi_smk": "🌿 Pembagian Rentang Nilai: Membagi tebakan angka berdasarkan rentang ('Jika pengalaman > 5 tahun, maka gaji = Rp 8 juta').",
            "tips_pemula": "Mudah diterjemahkan ke diagram alur keputusan bisnis.",
            "pros": ["Sederhana", "Visualisasi mudah"],
            "params": {
                "max_depth": {"type": "int", "default": 6, "min": 1, "max": 20, "step": 1, "label": "Kedalaman Maksimal", "smk_hint": "Batas cabang pertanyaan."}
            }
        },
        {
            "id": "ridge_regression",
            "name": "Ridge Regression (L2)",
            "icon": "🛡️",
            "badge": "Stabilizer Overfitting",
            "description": "Regresi linear dengan penalti L2 untuk mencegah bobot koefisien menjadi terlalu ekstrem saat multikolinearitas.",
            "analogi_smk": "🛡️ Garis Tren Berpelindung: Menarik garis tren dengan rem pengaman agar tidak terpengaruh oleh data ekstrim (outlier).",
            "tips_pemula": "Pilihan lebih stabil dibanding regresi linear biasa saat data berantakan.",
            "pros": ["Lebih stabil dibanding regresi linear standar"],
            "params": {
                "alpha": {"type": "float", "default": 1.0, "min": 0.01, "max": 20.0, "step": 0.5, "label": "Penalti Alpha (L2)", "smk_hint": "Kekuatan rem pengaman agar garis tidak miring berlebihan."}
            }
        }
    ]
}

def recommend_models(task_type, num_rows, num_features):
    """Memberikan rekomendasi algoritma cerdas berbasis profil dataset."""
    task_type = task_type.lower()
    models = AVAILABLE_MODELS.get(task_type, AVAILABLE_MODELS["classification"])
    
    recommendations = []
    
    if task_type == "classification":
        if num_rows < 150:
            recom_id = "random_forest"
            reason = f"Dataset berukuran kecil-menengah ({num_rows} baris). Random Forest sangat tangguh mengatasi variansi data tanpa mudah overfitting."
            alt_id = "logistic_regression"
            alt_reason = "Sebagai model baseline yang cepat dan mudah diverifikasi."
        elif num_rows < 1000:
            recom_id = "gradient_boosting"
            reason = f"Dataset berukuran {num_rows} baris dengan {num_features} fitur ideal untuk Gradient Boosting guna memaksimalkan akurasi dan F1-Score."
            alt_id = "random_forest"
            alt_reason = "Ensemble alternatif yang sangat stabil untuk dibandingkan."
        else:
            recom_id = "gradient_boosting"
            reason = f"Dataset cukup besar ({num_rows} baris). Algoritma boosting mampu menangkap pola kompleks dengan efisiensi komputasi tinggi."
            alt_id = "logistic_regression"
            alt_reason = "Logistic Regression sangat scalable untuk volume data tinggi."
    else: # regression
        if num_rows < 200:
            recom_id = "random_forest_regressor"
            reason = f"Untuk {num_rows} baris data regresi, Random Forest Regressor memberikan estimasi non-linear yang akurat tanpa sensitif terhadap outlier."
            alt_id = "linear_regression"
            alt_reason = "Linear Regression memberikan garis tren dasar sebagai pembanding."
        else:
            recom_id = "gradient_boosting_regressor"
            reason = f"Gradient Boosting Regressor direkomendasikan karena meminimalkan selisih prediksi (RMSE/MAE) secara iteratif pada {num_rows} baris data."
            alt_id = "random_forest_regressor"
            alt_reason = "Alternatif ensemble berbasis agregasi pohon."

    return {
        "primary_recommendation": {
            "model_id": recom_id,
            "reason": reason
        },
        "alternative_recommendation": {
            "model_id": alt_id,
            "reason": alt_reason
        },
        "all_models": models
    }
