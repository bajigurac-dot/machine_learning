import time
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

def instantiate_model(model_id, params=None):
    params = params or {}
    clean_params = {}
    
    # Clean and cast params
    for k, v in params.items():
        if v == "true" or v is True:
            clean_params[k] = True
        elif v == "false" or v is False:
            clean_params[k] = False
        else:
            try:
                if isinstance(v, str) and "." in v:
                    clean_params[k] = float(v)
                elif isinstance(v, str) and v.isdigit():
                    clean_params[k] = int(v)
                else:
                    clean_params[k] = v
            except (ValueError, TypeError):
                clean_params[k] = v

    # Classification
    if model_id == "random_forest":
        return RandomForestClassifier(
            n_estimators=int(clean_params.get("n_estimators", 100)),
            max_depth=int(clean_params.get("max_depth", 10)),
            random_state=int(clean_params.get("random_state", 42))
        )
    elif model_id == "gradient_boosting":
        return GradientBoostingClassifier(
            n_estimators=int(clean_params.get("n_estimators", 100)),
            learning_rate=float(clean_params.get("learning_rate", 0.1)),
            max_depth=int(clean_params.get("max_depth", 4)),
            random_state=42
        )
    elif model_id == "logistic_regression":
        return LogisticRegression(
            C=float(clean_params.get("C", 1.0)),
            max_iter=int(clean_params.get("max_iter", 200)),
            random_state=42
        )
    elif model_id == "decision_tree":
        return DecisionTreeClassifier(
            max_depth=int(clean_params.get("max_depth", 6)),
            min_samples_split=int(clean_params.get("min_samples_split", 2)),
            random_state=42
        )
    elif model_id == "knn":
        return KNeighborsClassifier(
            n_neighbors=int(clean_params.get("n_neighbors", 5)),
            weights=str(clean_params.get("weights", "uniform"))
        )
    elif model_id == "svc":
        return SVC(
            C=float(clean_params.get("C", 1.0)),
            kernel=str(clean_params.get("kernel", "rbf")),
            probability=True,
            random_state=42
        )
        
    # Regression
    elif model_id == "random_forest_regressor":
        return RandomForestRegressor(
            n_estimators=int(clean_params.get("n_estimators", 100)),
            max_depth=int(clean_params.get("max_depth", 10)),
            random_state=int(clean_params.get("random_state", 42))
        )
    elif model_id == "gradient_boosting_regressor":
        return GradientBoostingRegressor(
            n_estimators=int(clean_params.get("n_estimators", 100)),
            learning_rate=float(clean_params.get("learning_rate", 0.1)),
            max_depth=int(clean_params.get("max_depth", 4)),
            random_state=42
        )
    elif model_id == "linear_regression":
        return LinearRegression(
            fit_intercept=clean_params.get("fit_intercept", True)
        )
    elif model_id == "decision_tree_regressor":
        return DecisionTreeRegressor(
            max_depth=int(clean_params.get("max_depth", 6)),
            random_state=42
        )
    elif model_id == "ridge_regression":
        return Ridge(
            alpha=float(clean_params.get("alpha", 1.0)),
            random_state=42
        )
    else:
        raise ValueError(f"Model ID '{model_id}' tidak dikenal.")

def train_single_model(model_id, params, data_bundle):
    """Melatih satu model ML dan menghitung metrik evaluasi lengkap."""
    model = instantiate_model(model_id, params)
    
    X_train = data_bundle["X_train"]
    X_test = data_bundle["X_test"]
    y_train = data_bundle["y_train"]
    y_test = data_bundle["y_test"]
    task_type = data_bundle["task_type"]
    feature_names = data_bundle.get("feature_names", [])
    target_classes = data_bundle.get("target_classes")
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_duration = round(time.time() - start_time, 3)
    
    y_pred = model.predict(X_test)
    
    # Extract feature importance if model has it
    feature_importance = []
    if hasattr(model, "feature_importances_"):
        imps = model.feature_importances_
        sorted_indices = np.argsort(imps)[::-1][:10]
        for idx in sorted_indices:
            feature_importance.append({
                "feature": feature_names[idx] if idx < len(feature_names) else f"Feat_{idx}",
                "score": float(round(imps[idx], 4))
            })
    elif hasattr(model, "coef_"):
        coef = np.abs(model.coef_)
        if coef.ndim > 1:
            coef = np.mean(coef, axis=0)
        sorted_indices = np.argsort(coef)[::-1][:10]
        sum_c = np.sum(coef) if np.sum(coef) > 0 else 1.0
        for idx in sorted_indices:
            feature_importance.append({
                "feature": feature_names[idx] if idx < len(feature_names) else f"Feat_{idx}",
                "score": float(round(coef[idx] / sum_c, 4))
            })

    if task_type == "classification":
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
        
        cm = confusion_matrix(y_test, y_pred)
        cm_list = cm.tolist()
        
        # Friendly labels
        labels = target_classes if target_classes else [str(c) for c in np.unique(y_test)]
        
        metrics = {
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "score_display": f"{round(acc * 100, 2)}%",
            "primary_metric_name": "Akurasi",
            "primary_metric_value": round(acc * 100, 2),
            "confusion_matrix": {
                "matrix": cm_list,
                "labels": labels
            }
        }
    else: # regression
        r2 = float(r2_score(y_test, y_pred))
        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        
        # Sample actual vs predicted
        sample_preds = []
        sample_len = min(10, len(y_test))
        for i in range(sample_len):
            sample_preds.append({
                "actual": float(round(y_test[i], 2)),
                "predicted": float(round(y_pred[i], 2)),
                "diff": float(round(abs(y_test[i] - y_pred[i]), 2))
            })
            
        metrics = {
            "r2_score": round(r2, 4),
            "r2_percent": round(max(0, r2) * 100, 2),
            "mae": round(mae, 2),
            "mse": round(mse, 2),
            "rmse": round(rmse, 2),
            "score_display": f"R² = {round(r2, 3)}",
            "primary_metric_name": "R² Score",
            "primary_metric_value": round(r2, 4),
            "sample_predictions": sample_preds
        }
        
    return {
        "model": model,
        "model_id": model_id,
        "model_name": model.__class__.__name__,
        "metrics": metrics,
        "training_duration": training_duration,
        "feature_importance": feature_importance,
        "params": params
    }

def run_automl_benchmark(data_bundle):
    """Menjalankan pelatihan otomatis (AutoML) untuk seluruh model yang relevan dan menghasilkan leaderboard."""
    task_type = data_bundle["task_type"]
    
    if task_type == "classification":
        model_ids = ["random_forest", "gradient_boosting", "logistic_regression", "decision_tree", "knn"]
    else:
        model_ids = ["random_forest_regressor", "gradient_boosting_regressor", "linear_regression", "decision_tree_regressor", "ridge_regression"]
        
    leaderboard = []
    trained_models = {}
    
    for mid in model_ids:
        try:
            res = train_single_model(mid, {}, data_bundle)
            trained_models[mid] = res
            
            score = res["metrics"]["primary_metric_value"]
            metric_name = res["metrics"]["primary_metric_name"]
            score_disp = res["metrics"]["score_display"]
            
            leaderboard.append({
                "model_id": mid,
                "model_name": res["model_name"],
                "score": score,
                "score_display": score_disp,
                "metric_name": metric_name,
                "duration": res["training_duration"],
                "metrics": res["metrics"],
                "feature_importance": res["feature_importance"]
            })
        except Exception as e:
            print(f"Gagal melatih model {mid} di AutoML: {e}")
            
    # Sort leaderboard by score descending
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    
    # Assign ranks
    for rank, item in enumerate(leaderboard, 1):
        item["rank"] = rank
        item["is_winner"] = (rank == 1)
        
    winner_id = leaderboard[0]["model_id"] if leaderboard else None
    winner_result = trained_models.get(winner_id)
    
    return {
        "leaderboard": leaderboard,
        "winner": leaderboard[0] if leaderboard else None,
        "winner_result": winner_result,
        "total_models_trained": len(leaderboard)
    }
