import os
import sys
import io
import json
import datetime

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, Response

from ml_engine.datasets import get_available_datasets, load_dataset, parse_uploaded_file, ensure_sample_datasets
from ml_engine.preprocessor import analyze_dataframe, clean_dataframe, MLDataPipeline
from ml_engine.recommender import recommend_models, AVAILABLE_MODELS
from ml_engine.trainer import train_single_model, run_automl_benchmark
from ml_engine.code_generator import generate_python_script
from ml_engine.project_storage import (
    init_db, save_project, save_experiment, list_projects, get_project_details, delete_project
)
from ml_engine.ai_copilot import handle_ai_chat, generate_local_feature_spec, generate_local_prd, test_gemini_connection
from ml_engine.elearning import (
    init_elearning_db, list_active_exams, get_exam_details, create_exam, update_exam, delete_exam,
    add_question, get_question, update_question, delete_question, execute_python_code, execute_sql_query,
    get_sql_mock_schema,
    submit_exam_answers, list_submissions, update_submission_score, delete_submission,
    generate_scores_pdf,
    verify_student_login, get_student_by_nisn, get_student_exam_attempts,
    get_student_card_summary, generate_student_card_pdf,
    check_student_exam_attempt, list_all_students, add_student, delete_student,
    verify_admin_login, change_admin_password
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max upload
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Session state in memory
ACTIVE_SESSION = {
    "df": None,
    "dataset_name": "titanic",
    "target_column": "Survived",
    "task_type": "classification",
    "pipeline": None,
    "data_bundle": None,
    "active_model_result": None,
    "automl_result": None
}

def ensure_active_dataset():
    if ACTIVE_SESSION["df"] is None:
        try:
            df, target = load_dataset("titanic")
            ACTIVE_SESSION["df"] = df
            ACTIVE_SESSION["dataset_name"] = "titanic"
            ACTIVE_SESSION["target_column"] = target or "Survived"
            ACTIVE_SESSION["task_type"] = "classification"
        except Exception as e:
            print(f"Auto-init failed: {e}")

try:
    ensure_sample_datasets()
    ensure_active_dataset()
except Exception:
    pass

@app.route("/")
def index():
    return render_template("index.html")

# ==================== DATASET ENDPOINTS ====================

@app.route("/api/datasets", methods=["GET"])
def api_get_datasets():
    datasets = get_available_datasets()
    return jsonify({"success": True, "datasets": datasets})

@app.route("/api/dataset/load", methods=["POST"])
def api_load_dataset():
    data = request.json or {}
    dataset_id = data.get("dataset_id", "iris")
    
    try:
        df, default_target = load_dataset(dataset_id)
        ACTIVE_SESSION["df"] = df
        ACTIVE_SESSION["dataset_name"] = dataset_id
        ACTIVE_SESSION["target_column"] = default_target or df.columns[-1]
        ACTIVE_SESSION["pipeline"] = None
        ACTIVE_SESSION["data_bundle"] = None
        ACTIVE_SESSION["active_model_result"] = None
        
        analysis = analyze_dataframe(df)
        
        # Sample rows for table preview (first 10)
        table_preview = df.head(15).fillna("").to_dict(orient="records")
        
        return jsonify({
            "success": True,
            "dataset_name": dataset_id,
            "default_target": ACTIVE_SESSION["target_column"],
            "analysis": analysis,
            "table_preview": table_preview
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/dataset/upload", methods=["POST"])
def api_upload_dataset():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "Tidak ada file yang diunggah."}), 400
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Nama file kosong."}), 400
        
    try:
        df = parse_uploaded_file(file, file.filename)
        dataset_name = os.path.splitext(file.filename)[0]
        
        ACTIVE_SESSION["df"] = df
        ACTIVE_SESSION["dataset_name"] = dataset_name
        ACTIVE_SESSION["target_column"] = df.columns[-1]
        ACTIVE_SESSION["pipeline"] = None
        ACTIVE_SESSION["data_bundle"] = None
        ACTIVE_SESSION["active_model_result"] = None
        
        analysis = analyze_dataframe(df)
        table_preview = df.head(15).fillna("").to_dict(orient="records")
        
        return jsonify({
            "success": True,
            "dataset_name": dataset_name,
            "default_target": ACTIVE_SESSION["target_column"],
            "analysis": analysis,
            "table_preview": table_preview
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Gagal membaca file: {str(e)}"}), 400

@app.route("/api/dataset/clean", methods=["POST"])
def api_clean_dataset():
    if ACTIVE_SESSION["df"] is None:
        return jsonify({"success": False, "error": "Tidak ada dataset aktif."}), 400
        
    actions = request.json or {}
    try:
        df_cleaned = clean_dataframe(ACTIVE_SESSION["df"], actions)
        ACTIVE_SESSION["df"] = df_cleaned
        
        analysis = analyze_dataframe(df_cleaned)
        table_preview = df_cleaned.head(15).fillna("").to_dict(orient="records")
        
        return jsonify({
            "success": True,
            "message": "Data berhasil dibersihkan!",
            "analysis": analysis,
            "table_preview": table_preview
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# ==================== ML MODEL & TRAINING ENDPOINTS ====================

@app.route("/api/models/recommend", methods=["POST"])
def api_recommend_models():
    data = request.json or {}
    target_col = data.get("target_column") or ACTIVE_SESSION["target_column"]
    
    if ACTIVE_SESSION["df"] is None:
        return jsonify({"success": False, "error": "Belum ada dataset yang dimuat."}), 400
        
    df = ACTIVE_SESSION["df"]
    if target_col not in df.columns:
        return jsonify({"success": False, "error": f"Kolom {target_col} tidak ditemukan."}), 400
        
    ACTIVE_SESSION["target_column"] = target_col
    
    # Check task type
    from ml_engine.preprocessor import detect_task_type
    task_type = detect_task_type(df[target_col])
    ACTIVE_SESSION["task_type"] = task_type
    
    recom = recommend_models(task_type, len(df), len(df.columns) - 1)
    
    return jsonify({
        "success": True,
        "task_type": task_type,
        "target_column": target_col,
        "recommendations": recom
    })

@app.route("/api/train/single", methods=["POST"])
def api_train_single():
    if ACTIVE_SESSION["df"] is None:
        return jsonify({"success": False, "error": "Dataset belum dimuat."}), 400
        
    data = request.json or {}
    model_id = data.get("model_id")
    target_col = data.get("target_column") or ACTIVE_SESSION["target_column"]
    features = data.get("features")
    test_size = float(data.get("test_size", 0.2))
    params = data.get("params", {})
    
    try:
        pipeline = MLDataPipeline(target_col, feature_columns=features, test_size=test_size)
        data_bundle = pipeline.fit_transform(ACTIVE_SESSION["df"])
        
        ACTIVE_SESSION["pipeline"] = pipeline
        ACTIVE_SESSION["data_bundle"] = data_bundle
        ACTIVE_SESSION["target_column"] = target_col
        ACTIVE_SESSION["task_type"] = data_bundle["task_type"]
        
        result = train_single_model(model_id, params, data_bundle)
        ACTIVE_SESSION["active_model_result"] = result
        
        # Format response
        resp_data = {
            "model_id": result["model_id"],
            "model_name": result["model_name"],
            "task_type": data_bundle["task_type"],
            "metrics": result["metrics"],
            "training_duration": result["training_duration"],
            "feature_importance": result["feature_importance"],
            "original_features": data_bundle["original_features"],
            "target_classes": data_bundle["target_classes"],
            "rapor_smk": result.get("rapor_smk")
        }
        return jsonify({"success": True, "result": resp_data})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/train/automl", methods=["POST"])
def api_train_automl():
    if ACTIVE_SESSION["df"] is None:
        return jsonify({"success": False, "error": "Dataset belum dimuat."}), 400
        
    data = request.json or {}
    target_col = data.get("target_column") or ACTIVE_SESSION["target_column"]
    features = data.get("features")
    test_size = float(data.get("test_size", 0.2))
    
    try:
        pipeline = MLDataPipeline(target_col, feature_columns=features, test_size=test_size)
        data_bundle = pipeline.fit_transform(ACTIVE_SESSION["df"])
        
        ACTIVE_SESSION["pipeline"] = pipeline
        ACTIVE_SESSION["data_bundle"] = data_bundle
        ACTIVE_SESSION["target_column"] = target_col
        ACTIVE_SESSION["task_type"] = data_bundle["task_type"]
        
        automl_res = run_automl_benchmark(data_bundle)
        ACTIVE_SESSION["automl_result"] = automl_res
        
        if automl_res.get("winner_result"):
            ACTIVE_SESSION["active_model_result"] = automl_res["winner_result"]
            
        return jsonify({
            "success": True,
            "task_type": data_bundle["task_type"],
            "target_column": target_col,
            "leaderboard": automl_res["leaderboard"],
            "winner": automl_res["winner"],
            "original_features": data_bundle["original_features"]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 400

# ==================== LIVE PREDICTION SANDBOX ====================

@app.route("/api/predict", methods=["POST"])
def api_predict():
    if not ACTIVE_SESSION.get("active_model_result") or not ACTIVE_SESSION.get("pipeline"):
        return jsonify({"success": False, "error": "Belum ada model yang berhasil dilatih."}), 400
        
    input_data = request.json or {}
    model = ACTIVE_SESSION["active_model_result"]["model"]
    pipeline = ACTIVE_SESSION["pipeline"]
    task_type = ACTIVE_SESSION["task_type"]
    
    try:
        X_infer = pipeline.transform_single_input(input_data)
        pred = model.predict(X_infer)[0]
        
        prob_dict = {}
        if task_type == "classification" and hasattr(model, "predict_proba"):
            try:
                probs = model.predict_proba(X_infer)[0]
                classes = pipeline.target_classes_ or [f"Class {i}" for i in range(len(probs))]
                for c, p in zip(classes, probs):
                    prob_dict[str(c)] = round(float(p) * 100, 1)
            except Exception:
                pass
                
        # Decode prediction if classification
        if task_type == "classification" and pipeline.target_encoder is not None:
            try:
                display_pred = str(pipeline.target_encoder.inverse_transform([int(pred)])[0])
            except Exception:
                display_pred = str(pred)
        else:
            display_pred = f"{float(pred):,.2f}"
            
        return jsonify({
            "success": True,
            "prediction": display_pred,
            "raw_prediction": float(pred) if task_type == "regression" else int(pred),
            "probabilities": prob_dict,
            "task_type": task_type
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# ==================== CODE GENERATOR ====================

@app.route("/api/code/generate", methods=["GET"])
def api_generate_code():
    res = ACTIVE_SESSION.get("active_model_result")
    dataset_name = ACTIVE_SESSION.get("dataset_name", "dataset")
    target_col = ACTIVE_SESSION.get("target_column", "target")
    task_type = ACTIVE_SESSION.get("task_type", "classification")
    
    if not res:
        model_id = "random_forest"
        model_name = "RandomForestClassifier"
        params = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
        metrics = {"score_display": "N/A"}
        feat_names = []
    else:
        model_id = res["model_id"]
        model_name = res["model_name"]
        params = res["params"]
        metrics = res["metrics"]
        feat_names = ACTIVE_SESSION["data_bundle"]["feature_names"] if ACTIVE_SESSION["data_bundle"] else []
        
    script = generate_python_script(
        dataset_name=dataset_name,
        target_column=target_col,
        model_id=model_id,
        model_name=model_name,
        hyperparameters=params,
        metrics=metrics,
        task_type=task_type,
        feature_names=feat_names
    )
    return jsonify({"success": True, "script": script})

@app.route("/api/code/download", methods=["GET"])
def api_download_code():
    code_res = api_generate_code()
    script = code_res.get_json().get("script", "")
    return Response(
        script,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=studio_ml_pipeline.py"}
    )

# ==================== PROJECT STORAGE ====================

@app.route("/api/projects", methods=["GET"])
def api_list_projects():
    projects = list_projects()
    return jsonify({"success": True, "projects": projects})

@app.route("/api/projects/save", methods=["POST"])
def api_save_project():
    data = request.json or {}
    name = data.get("name", f"Proyek {ACTIVE_SESSION.get('dataset_name', 'ML')}")
    desc = data.get("description", "Dibuat di Studio ML Python")
    
    proj_id = save_project(
        name=name,
        description=desc,
        dataset_name=ACTIVE_SESSION.get("dataset_name", "iris"),
        target_column=ACTIVE_SESSION.get("target_column", "target"),
        task_type=ACTIVE_SESSION.get("task_type", "classification")
    )
    
    # If active model, save as experiment
    active_res = ACTIVE_SESSION.get("active_model_result")
    if active_res:
        save_experiment(
            project_id=proj_id,
            model_id=active_res["model_id"],
            model_name=active_res["model_name"],
            score=active_res["metrics"]["primary_metric_value"],
            score_display=active_res["metrics"]["score_display"],
            metrics=active_res["metrics"],
            params=active_res["params"],
            duration=active_res["training_duration"]
        )
        
    return jsonify({"success": True, "project_id": proj_id, "message": "Proyek berhasil disimpan!"})

@app.route("/api/projects/<int:project_id>", methods=["GET"])
def api_get_project(project_id):
    proj = get_project_details(project_id)
    if not proj:
        return jsonify({"success": False, "error": "Proyek tidak ditemukan."}), 404
    return jsonify({"success": True, "project": proj})

@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def api_delete_project(project_id):
    delete_project(project_id)
    return jsonify({"success": True, "message": "Proyek berhasil dihapus."})

# ==================== AI COPILOT ENDPOINTS ====================

@app.route("/api/ai/chat", methods=["POST"])
def api_ai_chat():
    data = request.json or {}
    message = data.get("message", "")
    history = data.get("history", [])
    api_key = data.get("api_key", "").strip()
    provider = data.get("provider", "local")
    
    # Extract current session context
    best_model_name = "Belum Ada"
    best_score_disp = "N/A"
    if ACTIVE_SESSION.get("active_model_result"):
        best_model_name = ACTIVE_SESSION["active_model_result"]["model_name"]
        best_score_disp = ACTIVE_SESSION["active_model_result"]["metrics"]["score_display"]
        
    current_context = {
        "dataset_name": ACTIVE_SESSION.get("dataset_name"),
        "target_column": ACTIVE_SESSION.get("target_column"),
        "task_type": ACTIVE_SESSION.get("task_type"),
        "best_model": best_model_name,
        "best_score": best_score_disp
    }
    
    res = handle_ai_chat(
        message=message,
        conversation_history=history,
        current_context=current_context,
        api_key=api_key,
        provider=provider,
        return_dict=True
    )
    
    return jsonify({
        "success": True, 
        "reply": res["reply"],
        "provider_used": res["provider_used"],
        "gemini_error": res.get("gemini_error")
    })

@app.route("/api/ai/test_gemini", methods=["POST"])
def api_test_gemini():
    data = request.json or {}
    api_key = data.get("api_key", "").strip()
    result = test_gemini_connection(api_key)
    return jsonify(result)

@app.route("/api/ai/generate_spec", methods=["POST"])
def api_generate_spec():
    data = request.json or {}
    feature_name = data.get("feature_name", "Fitur Baru")
    goal = data.get("goal", "")
    target_user = data.get("target_user", "")
    complexity = data.get("complexity", "Medium")
    
    current_context = {
        "dataset_name": ACTIVE_SESSION.get("dataset_name"),
        "target_column": ACTIVE_SESSION.get("target_column"),
        "task_type": ACTIVE_SESSION.get("task_type")
    }
    
    spec_md = generate_local_feature_spec(
        feature_name=feature_name,
        goal=goal,
        target_user=target_user,
        complexity=complexity,
        current_context=current_context
    )
    return jsonify({"success": True, "spec_markdown": spec_md})

@app.route("/api/ai/generate_prd", methods=["POST"])
def api_generate_prd():
    data = request.json or {}
    project_name = data.get("project_name", f"Proyek {ACTIVE_SESSION.get('dataset_name', 'ML')}")
    
    prd_md = generate_local_prd(
        project_name=project_name,
        dataset_name=ACTIVE_SESSION.get("dataset_name"),
        task_type=ACTIVE_SESSION.get("task_type"),
        target_col=ACTIVE_SESSION.get("target_column")
    )
    return jsonify({"success": True, "prd_markdown": prd_md})

@app.route("/api/ai/download_markdown", methods=["POST"])
def api_download_markdown():
    data = request.json or {}
    content = data.get("content", "")
    filename = data.get("filename", "dokumen_studio_ml.md")
    if not filename.endswith(".md"):
        filename += ".md"
        
    return Response(
        content,
        mimetype="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

# ==================== E-LEARNING & CBT EXAM ENDPOINTS ====================

@app.route("/api/elearning/admin/login", methods=["POST"])
def api_elearning_admin_login():
    try:
        data = request.json or {}
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        res = verify_admin_login(username, password)
        if not res.get("success"):
            return jsonify(res), 401
        return jsonify(res)
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

@app.route("/api/elearning/admin/change-password", methods=["POST"])
def api_elearning_admin_change_password():
    data = request.json or {}
    username = data.get("username", "guru").strip()
    old_password = data.get("old_password", "").strip()
    new_password = data.get("new_password", "").strip()
    confirm_password = data.get("confirm_password", "").strip()

    if not old_password or not new_password:
        return jsonify({"success": False, "error": "Password lama dan password baru wajib diisi."}), 400

    if new_password != confirm_password:
        return jsonify({"success": False, "error": "Konfirmasi password baru tidak cocok!"}), 400

    try:
        change_admin_password(username, old_password, new_password)
        return jsonify({"success": True, "message": "Password akun Guru berhasil diubah! Gunakan password baru untuk login selanjutnya."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/student/login", methods=["POST"])
def api_elearning_student_login():
    data = request.json or {}
    nisn = data.get("nisn", "").strip()
    name = data.get("name", "").strip()
    
    if not nisn:
        return jsonify({"success": False, "error": "NISN atau No. Induk siswa wajib diisi."}), 400
        
    res = verify_student_login(nisn, name if name else None)
    if not res["success"]:
        return jsonify(res), 401
    return jsonify(res)

@app.route("/api/elearning/student/check-nisn/<nisn>", methods=["GET"])
def api_elearning_check_nisn(nisn):
    student = get_student_by_nisn(nisn)
    if not student:
        return jsonify({
            "success": False, 
            "error": f"NISN '{nisn}' tidak terdaftar di database resmi siswa SMK Cahaya Pertiwi."
        }), 404
    attempts = get_student_exam_attempts(student["nisn"])
    return jsonify({
        "success": True, 
        "student": student,
        "attempted_exam_ids": [a["exam_id"] for a in attempts]
    })

@app.route("/api/elearning/student/attempts", methods=["GET"])
def api_elearning_student_attempts():
    nisn = request.args.get("nisn", "").strip()
    if not nisn:
        return jsonify({"success": False, "error": "Parameter nisn wajib diisi."}), 400
    attempts = get_student_exam_attempts(nisn)
    return jsonify({"success": True, "attempts": attempts})

@app.route("/api/elearning/student/card/data", methods=["GET"])
def api_elearning_student_card_data():
    nisn = request.args.get("nisn", "").strip()
    if not nisn:
        return jsonify({"success": False, "error": "Parameter nisn wajib diisi."}), 400
    card_data = get_student_card_summary(nisn)
    if not card_data:
        return jsonify({"success": False, "error": f"Siswa dengan NISN '{nisn}' tidak terdaftar di database."}), 404
    return jsonify({"success": True, "data": card_data})

@app.route("/api/elearning/student/card/pdf", methods=["GET"])
def api_elearning_student_card_pdf():
    nisn = request.args.get("nisn", "").strip()
    if not nisn:
        return jsonify({"success": False, "error": "Parameter nisn wajib diisi."}), 400
    try:
        pdf_buffer = generate_student_card_pdf(nisn)
        filename = f"Kartu_Nilai_KHS_{nisn}.pdf"
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/student/card/print", methods=["GET"])
def api_elearning_student_card_print():
    nisn = request.args.get("nisn", "").strip()
    if not nisn:
        return "Parameter nisn wajib diisi.", 400
    card_data = get_student_card_summary(nisn)
    if not card_data:
        return f"Siswa dengan NISN '{nisn}' tidak terdaftar di database.", 404
    now = datetime.datetime.now()
    print_date = now.strftime("%d-%m-%Y %H:%M WIB")
    sign_date = now.strftime("%d %B %Y")
    return render_template(
        "report_student_card.html",
        student=card_data["student"],
        attempts=card_data["attempts"],
        summary=card_data["summary"],
        print_date=print_date,
        sign_date=sign_date
    )

@app.route("/api/elearning/exams", methods=["GET"])
def api_elearning_get_exams():
    exams = list_active_exams()
    return jsonify({"success": True, "exams": exams})

@app.route("/api/elearning/exams/<int:exam_id>", methods=["GET"])
def api_elearning_get_exam(exam_id):
    exam = get_exam_details(exam_id, include_correct_answers=False)
    if not exam:
        return jsonify({"success": False, "error": "Ujian tidak ditemukan."}), 404
    return jsonify({"success": True, "exam": exam})

@app.route("/api/elearning/admin/exams/<int:exam_id>", methods=["GET"])
def api_elearning_admin_get_exam(exam_id):
    exam = get_exam_details(exam_id, include_correct_answers=True)
    if not exam:
        return jsonify({"success": False, "error": "Ujian tidak ditemukan."}), 404
    return jsonify({"success": True, "exam": exam})

@app.route("/api/elearning/admin/exams/<int:exam_id>", methods=["PUT"])
def api_elearning_admin_update_exam(exam_id):
    data = request.json or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    subject = data.get("subject", "").strip()
    duration = data.get("duration_minutes", 30)
    is_active = data.get("is_active", 1)

    if not title or not subject:
        return jsonify({"success": False, "error": "Judul ujian dan mata pelajaran wajib diisi."}), 400

    try:
        update_exam(exam_id, title, description, subject, duration, is_active)
        return jsonify({"success": True, "message": "Paket ujian berhasil diperbarui!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/exams/create", methods=["POST"])
def api_elearning_create_exam():
    data = request.json or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    subject = data.get("subject", "").strip()
    duration = data.get("duration_minutes", 30)
    
    if not title or not subject:
        return jsonify({"success": False, "error": "Judul ujian dan mata pelajaran wajib diisi."}), 400
        
    exam_id = create_exam(title, description, subject, duration)
    return jsonify({"success": True, "exam_id": exam_id, "message": "Paket ujian berhasil dibuat!"})

@app.route("/api/elearning/exams/<int:exam_id>", methods=["DELETE"])
def api_elearning_delete_exam(exam_id):
    delete_exam(exam_id)
    return jsonify({"success": True, "message": "Ujian berhasil dihapus."})

@app.route("/api/elearning/questions/<int:question_id>", methods=["GET"])
def api_elearning_get_question(question_id):
    q = get_question(question_id)
    if not q:
        return jsonify({"success": False, "error": "Butir soal tidak ditemukan."}), 404
    return jsonify({"success": True, "question": q})

@app.route("/api/elearning/questions/add", methods=["POST"])
def api_elearning_add_question():
    data = request.json or {}
    exam_id = data.get("exam_id")
    question_type = data.get("question_type", "mcq")
    question_text = data.get("question_text", "").strip()
    options = data.get("options", [])
    correct_answer = data.get("correct_answer", "").strip()
    starter_code = data.get("starter_code", "")
    expected_output = data.get("expected_output", "")
    points = data.get("points", 20)
    
    if not exam_id or not question_text:
        return jsonify({"success": False, "error": "ID ujian dan teks soal wajib diisi."}), 400
        
    qid = add_question(
        exam_id=exam_id,
        question_type=question_type,
        question_text=question_text,
        options=options,
        correct_answer=correct_answer,
        starter_code=starter_code,
        expected_output=expected_output,
        points=points
    )
    return jsonify({"success": True, "question_id": qid, "message": "Soal berhasil ditambahkan!"})

@app.route("/api/elearning/questions/<int:question_id>", methods=["PUT"])
def api_elearning_update_question(question_id):
    data = request.json or {}
    question_type = data.get("question_type", "mcq")
    question_text = data.get("question_text", "").strip()
    options = data.get("options", [])
    correct_answer = data.get("correct_answer", "").strip()
    starter_code = data.get("starter_code", "")
    expected_output = data.get("expected_output", "")
    points = data.get("points", 20)

    if not question_text:
        return jsonify({"success": False, "error": "Teks pertanyaan wajib diisi."}), 400

    try:
        update_question(
            question_id=question_id,
            question_type=question_type,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
            starter_code=starter_code,
            expected_output=expected_output,
            points=points
        )
        return jsonify({"success": True, "message": "Butir soal berhasil diperbarui!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/questions/<int:question_id>", methods=["DELETE"])
def api_elearning_delete_question(question_id):
    delete_question(question_id)
    return jsonify({"success": True, "message": "Soal berhasil dihapus."})

@app.route("/api/elearning/code/run", methods=["POST"])
def api_elearning_run_code():
    data = request.json or {}
    language = data.get("language", "python").lower()
    code_text = data.get("code", "")
    expected_output = data.get("expected_output")
    
    if language == "sql":
        res = execute_sql_query(code_text, expected_output)
    else:
        res = execute_python_code(code_text, expected_output)
        
    return jsonify({
        "success": res["success"],
        "is_correct": res["is_correct"],
        "actual_output": res["actual_output"],
        "expected_output": res.get("expected_output"),
        "columns": res.get("columns", []),
        "rows": res.get("rows", []),
        "row_count": res.get("row_count", 0),
        "execution_time_ms": res.get("execution_time_ms", 0),
        "feedback_detail": res.get("feedback_detail", ""),
        "error": res.get("error")
    })

@app.route("/api/elearning/sql/schema", methods=["GET"])
def api_elearning_sql_schema():
    try:
        tables = get_sql_mock_schema()
        return jsonify({"success": True, "tables": tables})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/elearning/submissions/submit", methods=["POST"])
def api_elearning_submit_exam():
    data = request.json or {}
    exam_id = data.get("exam_id")
    student_info = data.get("student_info", {})
    answers = data.get("answers", {})
    duration_seconds = data.get("duration_seconds", 0)
    
    if not exam_id or not student_info.get("name"):
        return jsonify({"success": False, "error": "Data siswa dan ID ujian wajib diisi."}), 400
        
    nisn = student_info.get("nisn", "").strip()
    # Cegah siswa mengulang ujian yang sudah diselesaikan
    existing_attempt = check_student_exam_attempt(nisn, exam_id)
    if existing_attempt:
        return jsonify({
            "success": False, 
            "error": f"Siswa dengan NISN {nisn} sudah pernah menyelesaikan ujian ini (Skor: {existing_attempt['score']}). Tidak dapat mengulang tanpa izin guru."
        }), 403

    try:
        result = submit_exam_answers(
            exam_id=exam_id,
            student_info=student_info,
            answers_dict=answers,
            duration_seconds=duration_seconds
        )
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/elearning/admin/submissions", methods=["GET"])
def api_elearning_get_submissions():
    exam_id = request.args.get("exam_id", type=int)
    class_name = request.args.get("class_name")
    date_str = request.args.get("date")
    subs = list_submissions(exam_id=exam_id, class_name=class_name, date_str=date_str)
    return jsonify({"success": True, "submissions": subs})

@app.route("/api/elearning/admin/submissions/<int:submission_id>", methods=["PUT", "POST"])
def api_elearning_update_submission(submission_id):
    data = request.json or {}
    score = data.get("score")
    if score is None:
        return jsonify({"success": False, "error": "Nilai baru wajib diisi."}), 400
    try:
        updated = update_submission_score(submission_id, score)
        return jsonify({"success": True, "data": updated, "message": f"Nilai berhasil diperbarui menjadi {updated['score']}!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/admin/submissions/<int:submission_id>", methods=["DELETE"])
def api_elearning_delete_submission(submission_id):
    try:
        delete_submission(submission_id)
        return jsonify({"success": True, "message": "Data nilai berhasil dihapus."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/admin/report/scores/pdf", methods=["GET"])
def api_elearning_export_scores_pdf():
    class_name = request.args.get("class_name")
    date_str = request.args.get("date")
    subs = list_submissions(class_name=class_name, date_str=date_str)
    
    pdf_buffer = generate_scores_pdf(subs, class_filter=class_name, date_filter=date_str)
    
    filename = "rekap_nilai_smk_cahaya_pertiwi.pdf"
    if class_name and class_name.strip() and class_name.strip().lower() != "semua":
        clean_cls = class_name.strip().replace(" ", "_").replace("-", "_")
        filename = f"rekap_nilai_{clean_cls}.pdf"
        
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )

@app.route("/api/elearning/admin/report/scores/print", methods=["GET"])
def api_elearning_print_scores():
    class_name = request.args.get("class_name")
    date_str = request.args.get("date")
    subs = list_submissions(class_name=class_name, date_str=date_str)
    return render_template(
        "report_scores.html",
        submissions=subs,
        class_filter=class_name,
        date_filter=date_str,
        today=datetime.date.today().strftime("%d %B %Y")
    )

@app.route("/api/elearning/admin/report/students/print", methods=["GET"])
def api_elearning_print_students():
    class_name = request.args.get("class_name")
    search_name = request.args.get("name") or request.args.get("q")
    students = list_all_students(class_name, search_name)
    now = datetime.datetime.now()
    return render_template(
        "report_students.html",
        students=students,
        class_filter=class_name or "",
        search_filter=search_name or "",
        total_students=len(students),
        today=now.strftime("%d %B %Y"),
        print_date=now.strftime("%d-%m-%Y %H:%M WIB")
    )

@app.route("/api/elearning/admin/students", methods=["GET"])
def api_elearning_get_students():
    class_name = request.args.get("class_name")
    search_name = request.args.get("name") or request.args.get("q")
    students = list_all_students(class_name, search_name)
    return jsonify({"success": True, "students": students})

@app.route("/api/elearning/admin/students", methods=["POST"])
def api_elearning_add_student():
    data = request.json or {}
    nisn = data.get("nisn", "").strip()
    name = data.get("name", "").strip()
    class_name = data.get("class_name", "").strip()
    try:
        sid = add_student(nisn, name, class_name)
        return jsonify({"success": True, "student_id": sid, "message": f"Siswa {name} ({nisn}) berhasil didaftarkan!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/elearning/admin/students/<int:student_id>", methods=["DELETE"])
def api_elearning_delete_student(student_id):
    try:
        delete_student(student_id)
        return jsonify({"success": True, "message": "Data siswa berhasil dihapus."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    ensure_sample_datasets()
    init_db()
    init_elearning_db()
    print("================================================================")
    print(">> Studio ML Python Server Aktif di http://127.0.0.1:5000")
    print("================================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)

