import unittest
import os
import json
import pandas as pd
import numpy as np

from ml_engine.datasets import ensure_sample_datasets, load_dataset, get_available_datasets
from ml_engine.preprocessor import analyze_dataframe, clean_dataframe, MLDataPipeline, detect_task_type
from ml_engine.recommender import recommend_models
from ml_engine.trainer import train_single_model, run_automl_benchmark
from ml_engine.code_generator import generate_python_script
from ml_engine.project_storage import save_project, save_experiment, list_projects, delete_project
from ml_engine.ai_copilot import generate_local_prd, generate_local_feature_spec, handle_ai_chat
from app import app

class TestStudioMLEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_sample_datasets()
        cls.client = app.test_client()

    def test_01_datasets(self):
        datasets = get_available_datasets()
        self.assertGreaterEqual(len(datasets), 5)
        
        df_iris, target_iris = load_dataset("iris")
        self.assertEqual(target_iris, "species")
        self.assertEqual(len(df_iris), 150)
        
        df_titanic, target_titanic = load_dataset("titanic")
        self.assertEqual(target_titanic, "Survived")
        self.assertGreater(len(df_titanic), 0)

    def test_02_preprocessor_and_pipeline(self):
        df, target = load_dataset("iris")
        analysis = analyze_dataframe(df)
        self.assertEqual(analysis["total_rows"], 150)
        self.assertEqual(analysis["total_cols"], 5)
        
        # Test cleaning
        df_clean = clean_dataframe(df, {"drop_duplicates": True})
        self.assertIsInstance(df_clean, pd.DataFrame)
        
        # Test pipeline
        pipe = MLDataPipeline(target_column="species", test_size=0.2)
        bundle = pipe.fit_transform(df)
        
        self.assertEqual(bundle["task_type"], "classification")
        self.assertEqual(len(bundle["X_train"]) + len(bundle["X_test"]), len(df))
        self.assertIn("setosa", bundle["target_classes"])
        
        # Test single inference transformation
        sample_input = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
        vec = pipe.transform_single_input(sample_input)
        self.assertEqual(vec.shape, (1, len(bundle["feature_names"])))

    def test_03_recommender(self):
        recom_clf = recommend_models("classification", 200, 5)
        self.assertIn("primary_recommendation", recom_clf)
        self.assertIn("all_models", recom_clf)
        
        recom_reg = recommend_models("regression", 200, 5)
        self.assertIn("primary_recommendation", recom_reg)

    def test_04_training_and_automl(self):
        df, target = load_dataset("iris")
        pipe = MLDataPipeline(target_column="species", test_size=0.2)
        bundle = pipe.fit_transform(df)
        
        # Single train
        result = train_single_model("random_forest", {"n_estimators": 50, "max_depth": 5}, bundle)
        self.assertEqual(result["model_id"], "random_forest")
        self.assertGreater(result["metrics"]["accuracy"], 80)
        self.assertIn("confusion_matrix", result["metrics"])
        
        # Test AutoML runner
        automl_res = run_automl_benchmark(bundle)
        self.assertGreaterEqual(len(automl_res["leaderboard"]), 4)
        self.assertIsNotNone(automl_res["winner"])
        self.assertTrue(automl_res["winner"]["is_winner"])

    def test_05_code_generator(self):
        script = generate_python_script(
            dataset_name="iris",
            target_column="species",
            model_id="random_forest",
            model_name="RandomForestClassifier",
            hyperparameters={"n_estimators": 100},
            metrics={"score_display": "95%"},
            task_type="classification"
        )
        self.assertIn("RandomForestClassifier", script)
        self.assertIn("run_pipeline()", script)

    def test_06_project_storage(self):
        proj_id = save_project("Test Proyek Unit", "Deskripsi Uji", "iris", "species", "classification")
        self.assertIsInstance(proj_id, int)
        
        exp_id = save_experiment(proj_id, "random_forest", "RandomForestClassifier", 96.5, "96.5%", {"accuracy": 96.5}, {}, 0.05)
        self.assertIsInstance(exp_id, int)
        
        projs = list_projects()
        self.assertTrue(any(p["id"] == proj_id for p in projs))
        
        deleted = delete_project(proj_id)
        self.assertTrue(deleted)

    def test_07_ai_copilot(self):
        # PRD generator
        prd = generate_local_prd("Proyek Uji ML", "titanic", "classification", "Survived")
        self.assertIn("PRD", prd)
        self.assertIn("Survived", prd)
        
        # Spec generator
        spec = generate_local_feature_spec("Auto Retrain", "Retrain model otomatis", "MLOps", "Medium")
        self.assertIn("# Spesifikasi Teknis Fitur", spec)
        self.assertIn("Given", spec)
        self.assertIn("Task Breakdown", spec)
        
        # Chat
        reply_prd = handle_ai_chat("Buatkan PRD lengkap", [], {"dataset_name": "titanic", "target_column": "Survived"})
        self.assertIn("PRD", reply_prd)
        
        reply_task = handle_ai_chat("Breakdown task sprint", [], {"dataset_name": "titanic", "target_column": "Survived"})
        self.assertIn("Sprint", reply_task)

    def test_08_flask_api_endpoints(self):
        # GET datasets
        res = self.client.get("/api/datasets")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        
        # POST load dataset
        res = self.client.post("/api/dataset/load", json={"dataset_id": "iris"})
        self.assertEqual(res.status_code, 200)
        
        # POST AutoML
        res = self.client.post("/api/train/automl", json={"target_column": "species"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("leaderboard", data)
        
        # POST Predict
        res = self.client.post("/api/predict", json={
            "sepal_length": 5.0, "sepal_width": 3.6, "petal_length": 1.4, "petal_width": 0.2
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("prediction", data)
        
        # POST AI Chat
        res = self.client.post("/api/ai/chat", json={"message": "Buatkan PRD"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("reply", data)
        
        # POST AI Spec
        res = self.client.post("/api/ai/generate_spec", json={"feature_name": "Export PDF"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("spec_markdown", data)

if __name__ == "__main__":
    unittest.main()
