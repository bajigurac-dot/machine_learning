import os
import io
import pandas as pd
import numpy as np

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "sample_data")

DATASET_METADATA = {
    "titanic": {
        "id": "titanic",
        "name": "Titanic Survival",
        "task_type": "classification",
        "default_target": "Survived",
        "description": "Prediksi keselamatan penumpang kapal Titanic berdasarkan umur, kelas tiket, jenis kelamin, dan tarif.",
        "icon": "🚢"
    },
    "iris": {
        "id": "iris",
        "name": "Iris Flower Classification",
        "task_type": "classification",
        "default_target": "species",
        "description": "Klasifikasi spesies bunga Iris (Setosa, Versicolor, Virginica) berdasarkan ukuran kelopak dan mahkota.",
        "icon": "🌸"
    },
    "salary": {
        "id": "salary",
        "name": "Prediksi Gaji & Pengalaman",
        "task_type": "regression",
        "default_target": "Salary",
        "description": "Estimasi besaran gaji profesional berdasarkan tahun pengalaman, tingkat pendidikan, dan usia.",
        "icon": "💼"
    },
    "customer_churn": {
        "id": "customer_churn",
        "name": "Customer Churn (Pelanggan Berhenti)",
        "task_type": "classification",
        "default_target": "Churn",
        "description": "Deteksi apakah pelanggan telekomunikasi/SaaS berpotensi berhenti berlangganan atau tetap aktif.",
        "icon": "👥"
    },
    "housing": {
        "id": "housing",
        "name": "Prediksi Harga Rumah",
        "task_type": "regression",
        "default_target": "Price",
        "description": "Prediksi nilai jual rumah berdasarkan luas tanah, jumlah kamar, lokasi, dan usia bangunan.",
        "icon": "🏡"
    },
    "diabetes": {
        "id": "diabetes",
        "name": "Skrining Risiko Diabetes",
        "task_type": "classification",
        "default_target": "Outcome",
        "description": "Prediksi indikasi diabetes pasien berdasarkan glukosa, tekanan darah, indeks massa tubuh (BMI), dan usia.",
        "icon": "🩺"
    }
}

def ensure_sample_datasets():
    """Memastikan file dataset bawaan tersedia di direktori static/sample_data."""
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    # 1. Iris
    iris_path = os.path.join(SAMPLE_DIR, "iris.csv")
    if not os.path.exists(iris_path):
        from sklearn.datasets import load_iris
        data = load_iris(as_frame=True)
        df_iris = data.frame
        df_iris.columns = [c.replace(" (cm)", "").replace(" ", "_") for c in df_iris.columns]
        target_names = {0: "setosa", 1: "versicolor", 2: "virginica"}
        df_iris["target"] = df_iris["target"].map(target_names)
        df_iris.rename(columns={"target": "species"}, inplace=True)
        df_iris.to_csv(iris_path, index=False)

    # 2. Titanic
    titanic_path = os.path.join(SAMPLE_DIR, "titanic.csv")
    if not os.path.exists(titanic_path):
        np.random.seed(42)
        n = 300
        pclass = np.random.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
        sex = np.random.choice(["male", "female"], size=n, p=[0.64, 0.36])
        age = np.random.normal(29, 13, size=n).clip(1, 75).round(1)
        # Introduce a few missing ages
        age[np.random.choice(n, 15, replace=False)] = np.nan
        sibsp = np.random.poisson(0.5, size=n).clip(0, 5)
        fare = (pclass == 1) * np.random.exponential(60, n) + \
               (pclass == 2) * np.random.exponential(25, n) + \
               (pclass == 3) * np.random.exponential(12, n) + 7.5
        fare = fare.round(2)
        embarked = np.random.choice(["Southampton", "Cherbourg", "Queenstown"], size=n, p=[0.7, 0.2, 0.1])
        # Survived logic (women & 1st class higher survival)
        prob_surv = 0.2 + 0.45 * (sex == "female") + 0.25 * (pclass == 1) - 0.15 * (pclass == 3)
        prob_surv = np.clip(prob_surv, 0.05, 0.95)
        survived = (np.random.rand(n) < prob_surv).astype(int)
        
        df_titanic = pd.DataFrame({
            "Pclass": pclass,
            "Sex": sex,
            "Age": age,
            "SibSp": sibsp,
            "Fare": fare,
            "Embarked": embarked,
            "Survived": survived
        })
        df_titanic.to_csv(titanic_path, index=False)

    # 3. Salary
    salary_path = os.path.join(SAMPLE_DIR, "salary.csv")
    if not os.path.exists(salary_path):
        np.random.seed(101)
        n = 200
        experience = np.random.uniform(0.5, 20.0, size=n).round(1)
        education = np.random.choice(["Bachelor", "Master", "PhD"], size=n, p=[0.6, 0.3, 0.1])
        edu_bonus = {"Bachelor": 0, "Master": 15000000, "PhD": 32000000}
        age = (22 + experience + np.random.normal(1, 2, n)).round(0).clip(22, 65)
        salary = (6000000 + experience * 2500000 + [edu_bonus[e] for e in education] + np.random.normal(0, 1500000, n)).round(-4)
        df_salary = pd.DataFrame({
            "YearsExperience": experience,
            "Education": education,
            "Age": age.astype(int),
            "Salary": salary.astype(int)
        })
        df_salary.to_csv(salary_path, index=False)

    # 4. Customer Churn
    churn_path = os.path.join(SAMPLE_DIR, "customer_churn.csv")
    if not os.path.exists(churn_path):
        np.random.seed(77)
        n = 350
        tenure = np.random.randint(1, 72, size=n)
        contract = np.random.choice(["Month-to-month", "One year", "Two year"], size=n, p=[0.55, 0.25, 0.20])
        monthly = np.random.uniform(25, 120, size=n).round(2)
        support = np.random.choice(["Yes", "No"], size=n, p=[0.4, 0.6])
        online_security = np.random.choice(["Yes", "No"], size=n, p=[0.35, 0.65])
        
        prob_churn = 0.35 - (tenure / 100) * 0.3 + (monthly / 120) * 0.3 - (contract != "Month-to-month") * 0.3
        prob_churn = np.clip(prob_churn, 0.05, 0.90)
        churn = np.where(np.random.rand(n) < prob_churn, "Yes", "No")
        
        df_churn = pd.DataFrame({
            "TenureMonths": tenure,
            "Contract": contract,
            "MonthlyCharges": monthly,
            "TechSupport": support,
            "OnlineSecurity": online_security,
            "Churn": churn
        })
        df_churn.to_csv(churn_path, index=False)

    # 5. Housing
    housing_path = os.path.join(SAMPLE_DIR, "housing.csv")
    if not os.path.exists(housing_path):
        np.random.seed(4242)
        n = 250
        sqft = np.random.randint(60, 450, size=n)
        bedrooms = np.random.choice([1, 2, 3, 4, 5], size=n, p=[0.1, 0.3, 0.4, 0.15, 0.05])
        bathrooms = np.random.choice([1, 2, 3, 4], size=n, p=[0.25, 0.5, 0.2, 0.05])
        location = np.random.choice(["Pusat Kota", "Pinggiran", "Suburban"], size=n, p=[0.35, 0.45, 0.2])
        loc_mult = {"Pusat Kota": 1.5, "Pinggiran": 1.1, "Suburban": 0.85}
        price = (sqft * 7500000 + bedrooms * 35000000 + bathrooms * 25000000) * [loc_mult[l] for l in location]
        price = (price + np.random.normal(0, 40000000, n)).round(-5).clip(250000000, 5000000000)
        
        df_housing = pd.DataFrame({
            "SquareMeters": sqft,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "Location": location,
            "Price": price.astype(int)
        })
        df_housing.to_csv(housing_path, index=False)

    # 6. Diabetes
    diabetes_path = os.path.join(SAMPLE_DIR, "diabetes.csv")
    if not os.path.exists(diabetes_path):
        from sklearn.datasets import load_diabetes
        raw = load_diabetes(as_frame=True).frame
        # Convert to a friendly classification dataset
        df_diab = raw.copy()
        df_diab["Outcome"] = (df_diab["target"] > df_diab["target"].median()).astype(int)
        df_diab.drop(columns=["target"], inplace=True)
        # Scale back to realistic medical values
        df_diab["Age"] = (df_diab["age"] * 50 + 45).round(0).astype(int).clip(20, 85)
        df_diab["BMI"] = (df_diab["bmi"] * 25 + 26).round(1).clip(16.0, 48.0)
        df_diab["BloodPressure"] = (df_diab["bp"] * 30 + 80).round(0).astype(int).clip(60, 140)
        df_diab["Glucose"] = (df_diab["s1"] * 50 + 120).round(0).astype(int).clip(70, 240)
        df_diab = df_diab[["Age", "BMI", "BloodPressure", "Glucose", "Outcome"]]
        df_diab.to_csv(diabetes_path, index=False)

def get_available_datasets():
    """Mengembalikan daftar dataset bawaan dengan metadata ringkas."""
    ensure_sample_datasets()
    result = []
    for key, meta in DATASET_METADATA.items():
        filepath = os.path.join(SAMPLE_DIR, f"{key}.csv")
        rows, cols = 0, 0
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                rows, cols = len(df), len(df.columns)
            except Exception:
                pass
        item = meta.copy()
        item["rows"] = rows
        item["cols"] = cols
        result.append(item)
    return result

def load_dataset(dataset_id_or_path):
    """Memuat dataframe dari ID sampel atau path lokal."""
    ensure_sample_datasets()
    if dataset_id_or_path in DATASET_METADATA:
        filepath = os.path.join(SAMPLE_DIR, f"{dataset_id_or_path}.csv")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset {dataset_id_or_path} tidak ditemukan.")
        df = pd.read_csv(filepath)
        return df, DATASET_METADATA[dataset_id_or_path]["default_target"]
    elif os.path.exists(dataset_id_or_path):
        if dataset_id_or_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(dataset_id_or_path)
        else:
            df = pd.read_csv(dataset_id_or_path)
        return df, None
    else:
        raise FileNotFoundError(f"File atau dataset {dataset_id_or_path} tidak ditemukan.")

def parse_uploaded_file(file_storage, filename):
    """Membaca file yang diunggah (CSV atau Excel) ke pandas DataFrame."""
    ext = os.path.splitext(filename)[1].lower()
    content = file_storage.read()
    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(io.BytesIO(content))
    elif ext in [".csv", ".txt"]:
        try:
            df = pd.read_csv(io.BytesIO(content))
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(content), encoding="latin1")
    else:
        raise ValueError(f"Format file '{ext}' tidak didukung. Harap gunakan CSV atau Excel (.xlsx).")
    return df
