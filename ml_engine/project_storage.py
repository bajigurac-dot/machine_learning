import sqlite3
import json
import os
import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "studio_ml.db")
DB_PATH = os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)

# Pastikan folder database ada jika diarahkan ke subfolder
if os.path.dirname(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            dataset_name TEXT,
            target_column TEXT,
            task_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            model_id TEXT,
            model_name TEXT,
            score REAL,
            score_display TEXT,
            metrics_json TEXT,
            params_json TEXT,
            duration REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        );
        """)
        conn.commit()

def save_project(name, description, dataset_name, target_column, task_type):
    init_db()
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO projects (name, description, dataset_name, target_column, task_type) VALUES (?, ?, ?, ?, ?)",
            (name, description, dataset_name, target_column, task_type)
        )
        conn.commit()
        return cursor.lastrowid

def save_experiment(project_id, model_id, model_name, score, score_display, metrics, params, duration):
    init_db()
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO experiments 
            (project_id, model_id, model_name, score, score_display, metrics_json, params_json, duration) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (project_id, model_id, model_name, score, score_display, json.dumps(metrics), json.dumps(params), duration)
        )
        conn.commit()
        return cursor.lastrowid

def list_projects():
    init_db()
    with get_db() as conn:
        rows = conn.execute("""
            SELECT p.*, COUNT(e.id) as experiment_count, MAX(e.score) as best_score
            FROM projects p
            LEFT JOIN experiments e ON p.id = e.project_id
            GROUP BY p.id
            ORDER BY p.created_at DESC
        """).fetchall()
        return [dict(r) for r in rows]

def get_project_details(project_id):
    init_db()
    with get_db() as conn:
        project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not project:
            return None
        experiments = conn.execute(
            "SELECT * FROM experiments WHERE project_id = ? ORDER BY score DESC, created_at DESC", 
            (project_id,)
        ).fetchall()
        
        exp_list = []
        for e in experiments:
            d = dict(e)
            d["metrics"] = json.loads(d["metrics_json"]) if d["metrics_json"] else {}
            d["params"] = json.loads(d["params_json"]) if d["params_json"] else {}
            exp_list.append(d)
            
        res = dict(project)
        res["experiments"] = exp_list
        return res

def delete_project(project_id):
    init_db()
    with get_db() as conn:
        conn.execute("DELETE FROM experiments WHERE project_id = ?", (project_id,))
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return True
