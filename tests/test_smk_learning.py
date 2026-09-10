import unittest
import json
from ml_engine.ai_copilot import (
    handle_ai_chat,
    generate_local_prd,
    generate_local_feature_spec
)
from app import app

class TestSMKLearningEngine(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()

    def test_looping_smk_guide(self):
        """Uji materi looping memuat analogi, skrip Python, panduan VS Code, dan tantangan mandiri."""
        reply = handle_ai_chat("bagaimana cara membuat looping di python", [], {})
        self.assertIn("latihan_looping.py", reply)
        self.assertIn("for putaran in range", reply)
        self.assertIn("VS Code", reply)
        self.assertIn("python latihan_looping.py", reply)
        self.assertIn("Tantangan Praktik Mandiri", reply)

    def test_if_else_smk_guide(self):
        """Uji materi percabangan if-else dengan studi kasus kelulusan nilai siswa SMK."""
        reply = handle_ai_chat("ajarkan percabangan kondisi if else", [], {})
        self.assertIn("latihan_kondisi.py", reply)
        self.assertIn("if nilai_kejuruan", reply)
        self.assertIn("VS Code", reply)
        self.assertIn("python latihan_kondisi.py", reply)

    def test_functions_smk_guide(self):
        """Uji materi fungsi def dengan parameter dan return value."""
        reply = handle_ai_chat("cara buat fungsi def di python", [], {})
        self.assertIn("latihan_fungsi.py", reply)
        self.assertIn("def ", reply)
        self.assertIn("return ", reply)
        self.assertIn("VS Code", reply)

    def test_list_dict_smk_guide(self):
        """Uji materi struktur data list & dict untuk data profil siswa SMK."""
        reply = handle_ai_chat("ajarkan list dan dictionary", [], {})
        self.assertIn("latihan_data.py", reply)
        self.assertIn("mata_pelajaran", reply)
        self.assertIn("profil_siswa", reply)

    def test_jobsheet_prd_generation(self):
        """Uji lembar kerja jobsheet PRD siswa SMK siap cetak/unduh."""
        prd = generate_local_prd("Proyek Looping & Rekursif", "titanic", "klasifikasi", "Survived")
        self.assertIn("Lembar Rencana Proyek & PRD Pembelajaran Siswa SMK", prd)
        self.assertIn("Thoriq Azis", prd)
        self.assertIn("Siswa SMK Jurusan RPL / TKJ / SIJA", prd)
        self.assertIn("Alat Pengembangan", prd)
        self.assertIn("Visual Studio Code (VS Code)", prd)
        self.assertIn("Rubrik Penilaian Mandiri Siswa SMK", prd)

    def test_first_ml_project_in_vscode(self):
        """Uji materi Machine Learning pertama di VS Code untuk siswa SMK."""
        reply = handle_ai_chat(
            "buat skrip machine learning pertama",
            [],
            {"dataset_name": "titanic", "target_column": "Survived", "best_model": "RandomForest", "best_score": "88%"}
        )
        self.assertIn("proyek_ml_smk.py", reply)
        self.assertIn("train_test_split", reply)
        self.assertIn("RandomForestClassifier", reply)
        self.assertIn("VS Code", reply)

    def test_database_sql_smk_guide(self):
        """Uji materi database relasional SQLite & SQL mencakup konsep, skrip Python, dan panduan VS Code."""
        reply = handle_ai_chat("ajarkan saya tentang database dan query sql di python", [], {})
        self.assertIn("latihan_11_database_sqlite.py", reply)
        self.assertIn("sqlite3", reply)
        self.assertIn("CREATE TABLE", reply)
        self.assertIn("INNER JOIN", reply)
        self.assertIn("VS Code", reply)
        self.assertIn("sekolah_smk.db", reply)
        self.assertIn("Tantangan Praktik Mandiri", reply)

        # Uji pemanggilan via nomor materi '11'
        reply_num = handle_ai_chat("11", [], {})
        self.assertIn("latihan_11_database_sqlite.py", reply_num)

        # Uji via REST API endpoint
        res = self.client.post("/api/ai/chat", json={
            "message": "saya ingin belajar database sql",
            "provider": "local"
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("latihan_11_database_sqlite.py", res.get_json()["reply"])

    def test_ai_dataset_explanation(self):
        """Uji penjelasan kurikulum kenapa 6 dataset (Titanic, Iris, Gaji, dll) dipilih dan petunjuk menu E-Learning."""
        reply = handle_ai_chat("kenapa harus titanic", [], {})
        self.assertIn("Titanic Survival", reply)
        self.assertIn("Iris Flower", reply)
        self.assertIn("Prediksi Gaji", reply)
        self.assertIn("Customer Churn", reply)
        self.assertIn("Harga Rumah", reply)
        self.assertIn("Skrining Diabetes", reply)
        self.assertIn("Menu E-Learning", reply)

        # Uji via REST API
        res = self.client.post("/api/ai/chat", json={
            "message": "jelaskan alasan kenapa harus data titanic",
            "provider": "local"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("Titanic Survival", data["reply"])
        self.assertIn("Menu E-Learning", data["reply"])

if __name__ == "__main__":
    unittest.main()
