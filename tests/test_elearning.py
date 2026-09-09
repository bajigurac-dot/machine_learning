import unittest
import json
from app import app
from ml_engine.elearning import (
    init_elearning_db,
    execute_python_code,
    execute_sql_query,
    list_active_exams,
    get_exam_details,
    create_exam,
    delete_exam,
    add_question,
    delete_question,
    submit_exam_answers,
    list_submissions
)

class TestELearningEngine(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        init_elearning_db()

    def test_01_execute_python_code_success(self):
        """Uji eksekusi kode Python yang benar dan cocok dengan target output."""
        code = "for i in range(1, 6): print(i)"
        expected = "1\n2\n3\n4\n5"
        res = execute_python_code(code, expected)
        self.assertTrue(res["success"])
        self.assertTrue(res["is_correct"])
        self.assertEqual(res["actual_output"], expected)

    def test_02_execute_python_code_incorrect_and_error(self):
        """Uji eksekusi kode Python yang salah atau menghasilkan error sintaks."""
        # Output tidak sesuai
        code_wrong = "print('Halo Dunia')"
        expected = "Selamat Pagi"
        res_wrong = execute_python_code(code_wrong, expected)
        self.assertTrue(res_wrong["success"])
        self.assertFalse(res_wrong["is_correct"])

        # Error sintaks / runtime
        code_err = "print(10 / 0)"
        res_err = execute_python_code(code_err, "10")
        self.assertFalse(res_err["success"])
        self.assertFalse(res_err["is_correct"])
        self.assertIn("ZeroDivisionError", res_err["error"])

    def test_02b_execute_python_code_security_sandbox(self):
        """Uji pemblokiran modul dan fungsi berbahaya oleh sandbox SMK."""
        # Blokir import os
        res_os = execute_python_code("import os\nprint(os.getcwd())")
        self.assertFalse(res_os["success"])
        self.assertIn("SecurityBlock", res_os["error"])
        self.assertIn("diblokir", res_os["error"])

        # Blokir open()
        res_open = execute_python_code("f = open('studio_ml.db', 'r')")
        self.assertFalse(res_open["success"])
        self.assertIn("SecurityBlock", res_open["error"])
        self.assertIn("open()", res_open["error"])

        # Blokir subprocess
        res_sub = execute_python_code("from subprocess import Popen")
        self.assertFalse(res_sub["success"])
        self.assertIn("SecurityBlock", res_sub["error"])

    def test_02c_execute_python_code_infinite_loop_timeout(self):
        """Uji penghentian otomatis pada perulangan tanpa henti (infinite loop)."""
        code_loop = "while True:\n    pass"
        res = execute_python_code(code_loop)
        self.assertFalse(res["success"])
        self.assertIn("TimeoutError", res["error"])
        self.assertIn("infinite loop", res["error"].lower())

    def test_02d_sqlite_wal_mode_active(self):
        """Uji mode WAL dan timeout aktif pada koneksi SQLite."""
        from ml_engine.elearning import get_db
        with get_db() as conn:
            mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            self.assertEqual(mode.lower(), "wal")

    def test_03_execute_sql_query(self):
        """Uji eksekusi query SQL pada in-memory SQLite lab SMK."""
        query = "SELECT nama, jurusan FROM siswa WHERE jurusan = 'RPL' ORDER BY id ASC"
        res = execute_sql_query(query)
        self.assertTrue(res["success"])
        self.assertGreater(len(res["rows"]), 0)
        self.assertIn("Ahmad Rizki", res["actual_output"])

        # Uji penolakan query non-SELECT
        drop_query = "DROP TABLE siswa"
        res_drop = execute_sql_query(drop_query)
        self.assertFalse(res_drop["success"])
        self.assertIn("Hanya perintah SELECT", res_drop["error"])

    def test_04_preset_exams_and_questions(self):
        """Uji keberadaan paket ujian bawaan (Kuis Mingguan & Ulangan Semester)."""
        exams = list_active_exams()
        self.assertGreaterEqual(len(exams), 2)
        
        exam1 = get_exam_details(exams[0]["id"])
        self.assertIsNotNone(exam1)
        self.assertGreater(len(exam1["questions"]), 0)

        # Cek tipe soal
        types = [q["question_type"] for q in exam1["questions"]]
        self.assertIn("mcq", types)
        self.assertTrue("code_python" in types or "code_sql" in types)

    def test_05_exam_crud(self):
        """Uji pembuatan, penambahan soal, dan penghapusan ujian oleh admin/guru."""
        exam_id = create_exam(
            title="Kuis Uji Coba Unit Test",
            description="Deskripsi ujian tes",
            subject="Python Unit Testing",
            duration_minutes=20
        )
        self.assertIsInstance(exam_id, int)

        qid = add_question(
            exam_id=exam_id,
            question_type="mcq",
            question_text="Berapa hasil dari 2 + 2?",
            options=["A. 3", "B. 4", "C. 5", "D. 6"],
            correct_answer="B",
            points=25
        )
        self.assertIsInstance(qid, int)

        details = get_exam_details(exam_id, include_correct_answers=True)
        self.assertEqual(len(details["questions"]), 1)
        self.assertEqual(details["questions"][0]["correct_answer"], "B")

        delete_question(qid)
        details_after = get_exam_details(exam_id)
        self.assertEqual(len(details_after["questions"]), 0)

        deleted = delete_exam(exam_id)
        self.assertTrue(deleted)

    def test_06_auto_grading_submission(self):
        """Uji penilaian otomatis lembar jawaban siswa dan kalkulasi nilai akhir."""
        exams = list_active_exams()
        exam_id = exams[0]["id"]
        exam = get_exam_details(exam_id, include_correct_answers=True)

        student = {
            "name": "Budi Penguji",
            "nisn": "12345678",
            "class_name": "XII RPL 1"
        }

        # Buat jawaban cerdas sesuai kunci
        answers = {}
        for q in exam["questions"]:
            if q["question_type"] == "mcq":
                answers[str(q["id"])] = q.get("correct_answer", "A")
            elif q["question_type"] == "code_python":
                answers[str(q["id"])] = f"print('{q.get('expected_output', '')}')" if q.get("expected_output") else "pass"
            elif q["question_type"] == "code_sql":
                answers[str(q["id"])] = "SELECT * FROM siswa"

        result = submit_exam_answers(exam_id, student, answers, duration_seconds=120)
        self.assertIn("score", result)
        self.assertIn("predicate", result)
        self.assertGreater(result["score"], 0)

        # Cek rekaman di database
        subs = list_submissions(exam_id)
        self.assertTrue(any(s["student_name"] == "Budi Penguji" for s in subs))

    def test_07_api_elearning_endpoints(self):
        """Uji endpoint REST API E-Learning."""
        # 1. GET Exams
        res = self.client.get("/api/elearning/exams")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreater(len(data["exams"]), 0)

        # 2. Live Run Code API
        res_code = self.client.post("/api/elearning/code/run", json={
            "language": "python",
            "code": "print('Tes SMK')",
            "expected_output": "Tes SMK"
        })
        self.assertEqual(res_code.status_code, 200)
        code_data = res_code.get_json()
        self.assertTrue(code_data["is_correct"])

        # 3. Admin Login API
        res_login_ok = self.client.post("/api/elearning/admin/login", json={
            "username": "guru",
            "password": "guru123"
        })
        self.assertEqual(res_login_ok.status_code, 200)
        self.assertTrue(res_login_ok.get_json()["success"])

        res_login_fail = self.client.post("/api/elearning/admin/login", json={
            "username": "guru",
            "password": "salahpassword"
        })
        self.assertEqual(res_login_fail.status_code, 401)

    def test_08_student_login_api(self):
        """Uji autentikasi login siswa terhadap Master Database Siswa resmi."""
        # 1. Login sukses dengan NISN dan nama resmi
        res_ok = self.client.post("/api/elearning/student/login", json={
            "name": "Thoriq Azis",
            "nisn": "006"
        })
        self.assertEqual(res_ok.status_code, 200)
        data = res_ok.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["student"]["name"], "Thoriq Azis")
        self.assertEqual(data["student"]["nisn"], "006")

        # 2. Login ditolak jika NISN fiktif / tidak terdaftar
        res_unregistered = self.client.post("/api/elearning/student/login", json={
            "name": "Siswa Ilegal",
            "nisn": "999999"
        })
        self.assertEqual(res_unregistered.status_code, 401)
        self.assertFalse(res_unregistered.get_json()["success"])
        self.assertIn("tidak terdaftar", res_unregistered.get_json()["error"])

        # 3. Login ditolak jika nama bertolak belakang dengan pemilik NISN resmi
        res_name_mismatch = self.client.post("/api/elearning/student/login", json={
            "name": "Nama Berbeda Total",
            "nisn": "006"
        })
        self.assertEqual(res_name_mismatch.status_code, 401)
        self.assertFalse(res_name_mismatch.get_json()["success"])

        # 4. Login gagal jika NISN kosong
        res_no_nisn = self.client.post("/api/elearning/student/login", json={
            "name": "Thoriq Azis",
            "nisn": ""
        })
        self.assertEqual(res_no_nisn.status_code, 400)
        self.assertFalse(res_no_nisn.get_json()["success"])

    def test_09_check_nisn_and_attempts_api(self):
        """Uji lookup instan NISN untuk autofill identitas siswa dan riwayat pengerjaan."""
        # 1. Check NISN terdaftar
        res_chk = self.client.get("/api/elearning/student/check-nisn/006")
        self.assertEqual(res_chk.status_code, 200)
        chk_data = res_chk.get_json()
        self.assertTrue(chk_data["success"])
        self.assertEqual(chk_data["student"]["name"], "Thoriq Azis")

        # 2. Check NISN tidak terdaftar
        res_chk_fake = self.client.get("/api/elearning/student/check-nisn/999999")
        self.assertEqual(res_chk_fake.status_code, 404)
        self.assertFalse(res_chk_fake.get_json()["success"])

        # 3. Riwayat attempts siswa
        res_att = self.client.get("/api/elearning/student/attempts?nisn=006")
        self.assertEqual(res_att.status_code, 200)
        self.assertTrue(res_att.get_json()["success"])

    def test_10_prevent_duplicate_submission(self):
        """Uji perlindungan integritas ujian: siswa tidak boleh mengulang ujian yang sudah dikerjakan."""
        import time
        unique_exam_id = create_exam(
            title=f"Ujian Isolasi Duplikat {time.time()}",
            description="Testing duplicate attempt protection",
            subject="Python Safety",
            duration_minutes=15
        )
        unique_student = {
            "name": "Siswa Tes Unik",
            "nisn": f"TEST_{int(time.time() * 1000)}",
            "class_name": "XII - SMK Cahaya Pertiwi"
        }

        # Submit pertama kali -> Sukses
        res1 = self.client.post("/api/elearning/submissions/submit", json={
            "exam_id": unique_exam_id,
            "student_info": unique_student,
            "answers": {},
            "duration_seconds": 60
        })
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(res1.get_json()["success"])

        # Submit kedua kali untuk ujian yang sama -> Ditolak (403 Forbidden)
        res2 = self.client.post("/api/elearning/submissions/submit", json={
            "exam_id": unique_exam_id,
            "student_info": unique_student,
            "answers": {},
            "duration_seconds": 90
        })
        self.assertEqual(res2.status_code, 403)
        self.assertFalse(res2.get_json()["success"])
        self.assertIn("sudah pernah menyelesaikan ujian", res2.get_json()["error"])

        delete_exam(unique_exam_id)

    def test_11_admin_student_crud(self):
        """Uji panel Master Data Siswa untuk Guru/Admin (List, Tambah, Hapus)."""
        import time
        unique_nisn = f"NISN_{int(time.time() * 1000) % 100000}"
        
        # 1. List siswa
        res_list = self.client.get("/api/elearning/admin/students")
        self.assertEqual(res_list.status_code, 200)
        students = res_list.get_json()["students"]
        self.assertGreater(len(students), 0)

        # 2. Daftarkan siswa baru
        res_add = self.client.post("/api/elearning/admin/students", json={
            "nisn": unique_nisn,
            "name": "Rian Saputra",
            "class_name": "XII - SMK Cahaya Pertiwi"
        })
        self.assertEqual(res_add.status_code, 200)
        new_sid = res_add.get_json()["student_id"]
        self.assertIsInstance(new_sid, int)

        # 3. Tolak jika mendaftarkan NISN yang sama (duplikat)
        res_dup = self.client.post("/api/elearning/admin/students", json={
            "nisn": unique_nisn,
            "name": "Rian Clone",
            "class_name": "XII - SMK Cahaya Pertiwi"
        })
        self.assertEqual(res_dup.status_code, 400)
        self.assertFalse(res_dup.get_json()["success"])

        # 4. Hapus siswa
        res_del = self.client.delete(f"/api/elearning/admin/students/{new_sid}")
        self.assertEqual(res_del.status_code, 200)
        self.assertTrue(res_del.get_json()["success"])

    def test_12_admin_submissions_filter(self):
        """Uji filter rekapitulasi nilai siswa berdasarkan kelas dan tanggal."""
        import datetime
        today_str = datetime.date.today().isoformat()

        # 1. Ambil seluruh submissions tanpa filter
        res_all = self.client.get("/api/elearning/admin/submissions")
        self.assertEqual(res_all.status_code, 200)
        subs_all = res_all.get_json()["submissions"]

        # 2. Filter berdasarkan kelas "XII - SMK Cahaya Pertiwi"
        res_class = self.client.get("/api/elearning/admin/submissions?class_name=XII%20-%20SMK%20Cahaya%20Pertiwi")
        self.assertEqual(res_class.status_code, 200)
        subs_class = res_class.get_json()["submissions"]
        for s in subs_class:
            self.assertIn("XII", s["student_class"])

        # 3. Filter berdasarkan tanggal hari ini
        res_date = self.client.get(f"/api/elearning/admin/submissions?date={today_str}")
        self.assertEqual(res_date.status_code, 200)
        subs_date = res_date.get_json()["submissions"]
        for s in subs_date:
            self.assertTrue(s["submitted_at"].startswith(today_str))

        # 4. Filter tanggal di masa depan yang tidak ada data (harus kosong)
        res_empty = self.client.get("/api/elearning/admin/submissions?date=2099-12-31")
        self.assertEqual(res_empty.status_code, 200)
        self.assertEqual(len(res_empty.get_json()["submissions"]), 0)

    def test_13_admin_edit_and_delete_submission(self):
        """Uji tombol aksi Guru/Admin: edit nilai ujian dan hapus rekaman nilai siswa."""
        import time
        unique_exam_id = create_exam(
            title=f"Ujian CRUD Nilai {time.time()}",
            description="Testing score edit and delete",
            subject="Python Score Actions",
            duration_minutes=15
        )
        unique_student = {
            "name": "Siswa Nilai Test",
            "nisn": f"TEST_SCORE_{int(time.time() * 1000)}",
            "class_name": "XII - SMK Cahaya Pertiwi"
        }

        # 1. Buat submission baru
        res_sub = self.client.post("/api/elearning/submissions/submit", json={
            "exam_id": unique_exam_id,
            "student_info": unique_student,
            "answers": {},
            "duration_seconds": 45
        })
        self.assertEqual(res_sub.status_code, 200)
        sub_id = res_sub.get_json()["result"]["submission_id"]

        # 2. Edit nilai menjadi 88.5 (Kompeten)
        res_edit = self.client.put(f"/api/elearning/admin/submissions/{sub_id}", json={
            "score": 88.5
        })
        self.assertEqual(res_edit.status_code, 200)
        edit_data = res_edit.get_json()
        self.assertTrue(edit_data["success"])
        self.assertEqual(edit_data["data"]["score"], 88.5)
        self.assertTrue(edit_data["data"]["is_passed"])

        # 3. Uji validasi nilai di luar batas (misal: 150 atau -10)
        res_invalid = self.client.put(f"/api/elearning/admin/submissions/{sub_id}", json={
            "score": 150
        })
        self.assertEqual(res_invalid.status_code, 400)
        self.assertFalse(res_invalid.get_json()["success"])

        # 4. Hapus rekaman nilai
        res_del = self.client.delete(f"/api/elearning/admin/submissions/{sub_id}")
        self.assertEqual(res_del.status_code, 200)
        self.assertTrue(res_del.get_json()["success"])

        # 5. Verifikasi setelah dihapus, siswa diizinkan mengerjakan kembali
        res_retry = self.client.post("/api/elearning/submissions/submit", json={
            "exam_id": unique_exam_id,
            "student_info": unique_student,
            "answers": {},
            "duration_seconds": 50
        })
        self.assertEqual(res_retry.status_code, 200)
        self.assertTrue(res_retry.get_json()["success"])

        delete_exam(unique_exam_id)

    def test_14_pdf_report_export(self):
        """Uji ekspor dan cetak laporan PDF resmi rekapitulasi nilai siswa."""
        # 1. Endpoint unduh berkas PDF biner asli
        res_pdf = self.client.get("/api/elearning/admin/report/scores/pdf")
        self.assertEqual(res_pdf.status_code, 200)
        self.assertEqual(res_pdf.content_type, "application/pdf")
        self.assertTrue(res_pdf.data.startswith(b"%PDF-"))
        self.assertGreater(len(res_pdf.data), 1000)

        # 2. Endpoint unduh PDF dengan filter kelas & tanggal
        import datetime
        today_str = datetime.date.today().isoformat()
        res_filtered_pdf = self.client.get(f"/api/elearning/admin/report/scores/pdf?class_name=XII%20-%20SMK%20Cahaya%20Pertiwi&date={today_str}")
        self.assertEqual(res_filtered_pdf.status_code, 200)
        self.assertEqual(res_filtered_pdf.content_type, "application/pdf")
        self.assertTrue(res_filtered_pdf.data.startswith(b"%PDF-"))

        # 3. Endpoint pratinjau cetak HTML
        res_print = self.client.get("/api/elearning/admin/report/scores/print")
        self.assertEqual(res_print.status_code, 200)
        self.assertIn(b"SMK CAHAYA PERTIWI", res_print.data)
        self.assertIn(b"LAPORAN REKAPITULASI NILAI", res_print.data)

    def test_15_admin_change_password(self):
        """Uji fitur ubah password akun Guru / Admin secara dinamis dan aman."""
        # 1. Login awal menggunakan password default
        res_login_init = self.client.post("/api/elearning/admin/login", json={
            "username": "guru",
            "password": "guru123"
        })
        self.assertEqual(res_login_init.status_code, 200)
        self.assertTrue(res_login_init.get_json()["success"])

        # 2. Gagal jika password lama salah
        res_wrong_old = self.client.post("/api/elearning/admin/change-password", json={
            "username": "guru",
            "old_password": "passwordsalah123",
            "new_password": "passwordBaru789",
            "confirm_password": "passwordBaru789"
        })
        self.assertEqual(res_wrong_old.status_code, 400)
        self.assertFalse(res_wrong_old.get_json()["success"])
        self.assertIn("Password lama", res_wrong_old.get_json()["error"])

        # 3. Gagal jika konfirmasi password tidak cocok
        res_mismatch = self.client.post("/api/elearning/admin/change-password", json={
            "username": "guru",
            "old_password": "guru123",
            "new_password": "passwordBaru789",
            "confirm_password": "passwordBeda789"
        })
        self.assertEqual(res_mismatch.status_code, 400)
        self.assertFalse(res_mismatch.get_json()["success"])
        self.assertIn("Konfirmasi password", res_mismatch.get_json()["error"])

        # 4. Gagal jika password baru kurang dari 5 karakter
        res_short = self.client.post("/api/elearning/admin/change-password", json={
            "username": "guru",
            "old_password": "guru123",
            "new_password": "123",
            "confirm_password": "123"
        })
        self.assertEqual(res_short.status_code, 400)
        self.assertFalse(res_short.get_json()["success"])

        # 5. Sukses ubah password ke "guruBaru2026!"
        res_success = self.client.post("/api/elearning/admin/change-password", json={
            "username": "guru",
            "old_password": "guru123",
            "new_password": "guruBaru2026!",
            "confirm_password": "guruBaru2026!"
        })
        self.assertEqual(res_success.status_code, 200)
        self.assertTrue(res_success.get_json()["success"])

        # 6. Login dengan password lama harus DITOLAK
        res_old_login = self.client.post("/api/elearning/admin/login", json={
            "username": "guru",
            "password": "guru123"
        })
        self.assertEqual(res_old_login.status_code, 401)
        self.assertFalse(res_old_login.get_json()["success"])

        # 7. Login dengan password baru harus BERHASIL
        res_new_login = self.client.post("/api/elearning/admin/login", json={
            "username": "guru",
            "password": "guruBaru2026!"
        })
        self.assertEqual(res_new_login.status_code, 200)
        self.assertTrue(res_new_login.get_json()["success"])

        # 8. Kembalikan password ke "guru123" agar pengujian berikutnya tetap konsisten
        res_revert = self.client.post("/api/elearning/admin/change-password", json={
            "username": "guru",
            "old_password": "guruBaru2026!",
            "new_password": "guru123",
            "confirm_password": "guru123"
        })
        self.assertEqual(res_revert.status_code, 200)
        self.assertTrue(res_revert.get_json()["success"])

    def test_16_student_grade_card(self):
        """Uji fitur login siswa dan melihat kartu nilai / KHS mandiri siswa."""
        # 1. Ambil kartu nilai siswa bawaan (Thoriq Azis - NISN 006)
        res_card = self.client.get("/api/elearning/student/card/data?nisn=006")
        self.assertEqual(res_card.status_code, 200)
        card_json = res_card.get_json()
        self.assertTrue(card_json["success"])
        self.assertEqual(card_json["data"]["student"]["name"], "Thoriq Azis")
        self.assertEqual(card_json["data"]["summary"]["kkm"], 75.0)

        # 2. Penolakan jika NISN tidak diisi
        res_no_nisn = self.client.get("/api/elearning/student/card/data")
        self.assertEqual(res_no_nisn.status_code, 400)
        self.assertFalse(res_no_nisn.get_json()["success"])

        # 3. Penolakan jika NISN tidak terdaftar
        res_unregistered = self.client.get("/api/elearning/student/card/data?nisn=NONEXISTENT_99999")
        self.assertEqual(res_unregistered.status_code, 404)
        self.assertFalse(res_unregistered.get_json()["success"])

        # 4. Uji berkas PDF Kartu Nilai Siswa (ReportLab)
        res_pdf = self.client.get("/api/elearning/student/card/pdf?nisn=006")
        self.assertEqual(res_pdf.status_code, 200)
        self.assertEqual(res_pdf.content_type, "application/pdf")
        self.assertTrue(res_pdf.data.startswith(b"%PDF-"))
        self.assertGreater(len(res_pdf.data), 1000)

        # 5. Uji pratinjau cetak HTML Kartu Nilai Siswa
        res_print = self.client.get("/api/elearning/student/card/print?nisn=006")
        self.assertEqual(res_print.status_code, 200)
        self.assertIn(b"SMK CAHAYA PERTIWI", res_print.data)
        self.assertIn(b"KARTU HASIL UJIAN", res_print.data)
        self.assertIn(b"Thoriq Azis", res_print.data)

        # 6. Uji siswa baru yang mengerjakan ujian dan verifikasi perhitungan kartu nilainya
        import time
        test_exam_id = create_exam(
            title=f"Ujian Evaluasi KHS {time.time()}",
            description="Testing student grade card score updates",
            subject="Python KHS Test",
            duration_minutes=20
        )
        test_nisn = f"KHS_{int(time.time() * 1000) % 100000}"
        from ml_engine.elearning import add_student
        add_student(test_nisn, "Siswa Uji KHS", "XII - SMK Cahaya Pertiwi")

        # Submit ujian dengan nilai 90 (Kompeten)
        res_sub = self.client.post("/api/elearning/submissions/submit", json={
            "exam_id": test_exam_id,
            "student_info": {
                "name": "Siswa Uji KHS",
                "nisn": test_nisn,
                "class_name": "XII - SMK Cahaya Pertiwi"
            },
            "answers": {},
            "duration_seconds": 120
        })
        self.assertEqual(res_sub.status_code, 200)
        sub_id = res_sub.get_json()["result"]["submission_id"]

        # Edit skor menjadi 92.5
        self.client.put(f"/api/elearning/admin/submissions/{sub_id}", json={"score": 92.5})

        # Cek data kartu nilai siswa uji
        res_check = self.client.get(f"/api/elearning/student/card/data?nisn={test_nisn}")
        self.assertEqual(res_check.status_code, 200)
        check_data = res_check.get_json()["data"]
        self.assertEqual(check_data["summary"]["total_exams"], 1)
        self.assertEqual(check_data["summary"]["average_score"], 92.5)
        self.assertTrue(check_data["summary"]["overall_passed"])
        self.assertEqual(len(check_data["attempts"]), 1)

        delete_exam(test_exam_id)

if __name__ == "__main__":
    unittest.main()
