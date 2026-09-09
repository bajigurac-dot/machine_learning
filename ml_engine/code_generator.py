def generate_python_script(dataset_name, target_column, model_id, model_name, hyperparameters, metrics, task_type, feature_names=None):
    """Menghasilkan skrip Python mandiri berbasis Scikit-Learn yang siap dieksekusi."""
    feature_names = feature_names or []
    
    # Model import mapping
    import_map = {
        "random_forest": "from sklearn.ensemble import RandomForestClassifier",
        "gradient_boosting": "from sklearn.ensemble import GradientBoostingClassifier",
        "logistic_regression": "from sklearn.linear_model import LogisticRegression",
        "decision_tree": "from sklearn.tree import DecisionTreeClassifier",
        "knn": "from sklearn.neighbors import KNeighborsClassifier",
        "svc": "from sklearn.svm import SVC",
        "random_forest_regressor": "from sklearn.ensemble import RandomForestRegressor",
        "gradient_boosting_regressor": "from sklearn.ensemble import GradientBoostingRegressor",
        "linear_regression": "from sklearn.linear_model import LinearRegression",
        "decision_tree_regressor": "from sklearn.tree import DecisionTreeRegressor",
        "ridge_regression": "from sklearn.linear_model import Ridge"
    }
    
    model_import = import_map.get(model_id, "from sklearn.ensemble import RandomForestClassifier")
    
    # Model instantiation string
    param_strs = []
    for k, v in hyperparameters.items():
        if isinstance(v, str) and not v.replace('.', '', 1).isdigit() and v not in ["True", "False"]:
            param_strs.append(f'{k}="{v}"')
        else:
            param_strs.append(f"{k}={v}")
    param_code = ", ".join(param_strs) if param_strs else ""
    
    if task_type == "classification":
        eval_metrics_import = "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix"
        target_prep_code = """    # Encoding label target untuk klasifikasi
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y.astype(str))"""
        eval_code = """# 5. Evaluasi Performa Model
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\\n=== HASIL EVALUASI MODEL ===")
print(f"Akurasi Pengujian: {acc * 100:.2f}%")
print("\\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred))
print("\\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))"""
    else:
        eval_metrics_import = "from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error"
        target_prep_code = """    # Format target numerik
    y = y.astype(float).values"""
        eval_code = """# 5. Evaluasi Performa Model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(f"\\n=== HASIL EVALUASI MODEL ===")
print(f"R-Squared (R²): {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")"""

    script = f'''\"\"\"
================================================================================
Studio ML Python - Skrip Pelatihan Otomatis
Dihasilkan secara otomatis untuk model: {model_name}
Dataset: {dataset_name} | Target: {target_column} | Task: {task_type.capitalize()}
================================================================================
\"\"\"

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
{model_import}
{eval_metrics_import}

def run_pipeline():
    print("Memulai proses pelatihan Machine Learning...")
    
    # 1. Memuat Dataset
    # Ganti path di bawah ini dengan file data Anda
    data_path = "{dataset_name}.csv"
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"File {{data_path}} tidak ditemukan di folder lokal. Harap sesuaikan lokasi file.")
        return
        
    print(f"Data berhasil dimuat. Dimensi: {{df.shape[0]}} baris, {{df.shape[1]}} kolom.")
    
    # 2. Pembersihan & Pra-pemrosesan Data
    target_col = "{target_column}"
    df = df.dropna(subset=[target_col]).drop_duplicates()
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Pisahkan kolom numerik dan kategorikal
    num_cols = X.select_dtypes(include=[np.number]).columns
    cat_cols = X.select_dtypes(exclude=[np.number]).columns
    
    # Imputasi nilai hilang sederhana
    for col in num_cols:
        X[col] = X[col].fillna(X[col].median())
    for col in cat_cols:
        X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else "Unknown")
        
    # One-Hot Encoding untuk fitur teks/kategorikal
    if len(cat_cols) > 0:
        X = pd.get_dummies(X, columns=cat_cols, drop_first=False)
        
    X = X.astype(float)
    
{target_prep_code}
    
    # 3. Pembagian Data Train dan Test (80:20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Ukuran Data Latih: {{len(X_train)}} | Ukuran Data Uji: {{len(X_test)}}")
    
    # 4. Inisialisasi & Pelatihan Model
    print(f"Melatih model {model_name}...")
    model = {model_name}({param_code})
    model.fit(X_train, y_train)
    print("Pelatihan selesai!")
    
    {eval_code}
    
    # 6. Menyimpan Model Terlatih
    model_filename = "model_{model_id}.joblib"
    joblib.dump(model, model_filename)
    print(f"\\nModel berhasil disimpan sebagai '{{model_filename}}'.")
    
    # 7. Contoh Inferensi Prediksi Baru
    print("\\nMelakukan uji prediksi 1 sampel baru...")
    sample_input = X_test.iloc[[0]]
    prediction = model.predict(sample_input)
    print(f"Hasil Prediksi Sampel: {{prediction[0]}}")

if __name__ == "__main__":
    run_pipeline()
'''
    return script
