import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def analyze_dataframe(df):
    """Menganalisis karakteristik umum dan statistik setiap kolom DataFrame."""
    total_rows = len(df)
    total_cols = len(df.columns)
    duplicate_count = int(df.duplicated().sum())
    
    columns_info = []
    for col in df.columns:
        s = df[col]
        missing_count = int(s.isnull().sum())
        missing_pct = round((missing_count / total_rows) * 100, 2) if total_rows > 0 else 0
        unique_vals = int(s.nunique(dropna=True))
        
        # Determine column general type
        if pd.api.types.is_bool_dtype(s):
            col_type = "boolean"
        elif pd.api.types.is_numeric_dtype(s):
            col_type = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(s):
            col_type = "datetime"
        else:
            col_type = "categorical"
            
        col_stat = {
            "name": col,
            "type": col_type,
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "unique_count": unique_vals,
            "sample_values": [str(v) for v in s.dropna().head(5).tolist()]
        }
        
        if col_type == "numeric":
            clean_s = s.dropna()
            if len(clean_s) > 0:
                col_stat["stats"] = {
                    "min": float(clean_s.min()),
                    "max": float(clean_s.max()),
                    "mean": float(round(clean_s.mean(), 2)),
                    "median": float(round(clean_s.median(), 2)),
                    "std": float(round(clean_s.std(), 2)) if len(clean_s) > 1 else 0.0
                }
        else:
            top_vals = s.value_counts(dropna=True).head(4).to_dict()
            col_stat["top_values"] = {str(k): int(v) for k, v in top_vals.items()}
            
        columns_info.append(col_stat)
        
    return {
        "total_rows": total_rows,
        "total_cols": total_cols,
        "duplicate_rows": duplicate_count,
        "columns": columns_info
    }

def detect_task_type(series):
    """Mendeteksi apakah kolom target berupa 'classification' atau 'regression'."""
    clean_s = series.dropna()
    unique_count = clean_s.nunique()
    
    if pd.api.types.is_bool_dtype(clean_s) or not pd.api.types.is_numeric_dtype(clean_s):
        return "classification"
    
    # If numeric but only a few discrete integer values (e.g. 0, 1 or classes 1, 2, 3)
    if unique_count <= 10 and (clean_s % 1 == 0).all():
        return "classification"
        
    return "regression"

def clean_dataframe(df, actions=None):
    """Membersihkan DataFrame berdasarkan opsi yang ditentukan."""
    actions = actions or {}
    df_clean = df.copy()
    
    # 1. Hapus duplikat
    if actions.get("drop_duplicates", True):
        df_clean = df_clean.drop_duplicates()
        
    # 2. Hapus kolom yang tidak diinginkan
    drop_cols = actions.get("drop_columns", [])
    if drop_cols:
        existing_drop = [c for c in drop_cols if c in df_clean.columns]
        df_clean = df_clean.drop(columns=existing_drop)
        
    # 3. Imputasi nilai hilang
    numeric_strategy = actions.get("missing_numeric", "median")
    cat_strategy = actions.get("missing_categorical", "mode")
    
    num_cols = df_clean.select_dtypes(include=[np.number]).columns
    cat_cols = df_clean.select_dtypes(exclude=[np.number]).columns
    
    for c in num_cols:
        if df_clean[c].isnull().any():
            if numeric_strategy == "mean":
                df_clean[c] = df_clean[c].fillna(df_clean[c].mean())
            elif numeric_strategy == "median":
                df_clean[c] = df_clean[c].fillna(df_clean[c].median())
            elif numeric_strategy == "zero":
                df_clean[c] = df_clean[c].fillna(0)
            elif numeric_strategy == "drop":
                df_clean = df_clean.dropna(subset=[c])
                
    for c in cat_cols:
        if df_clean[c].isnull().any():
            if cat_strategy == "mode":
                mode_val = df_clean[c].mode().iloc[0] if not df_clean[c].mode().empty else "Unknown"
                df_clean[c] = df_clean[c].fillna(mode_val)
            elif cat_strategy == "unknown":
                df_clean[c] = df_clean[c].fillna("Unknown")
            elif cat_strategy == "drop":
                df_clean = df_clean.dropna(subset=[c])
                
    return df_clean

class MLDataPipeline:
    """Mengelola transformasi data tabular mentah menjadi fitur ML siap latih dan inferensi."""
    def __init__(self, target_column, feature_columns=None, test_size=0.2, random_state=42):
        self.target_column = target_column
        self.feature_columns = feature_columns
        self.test_size = test_size
        self.random_state = random_state
        
        self.task_type = None
        self.numeric_cols = []
        self.categorical_cols = []
        self.num_imputer = None
        self.cat_imputer = None
        self.scaler = None
        self.target_encoder = None
        self.target_classes_ = None
        self.processed_feature_names = []
        self.cat_dummy_columns = []
        self.numeric_medians = {}
        self.cat_modes = {}
        self.training_feature_columns = []

    def fit_transform(self, df):
        if self.target_column not in df.columns:
            raise ValueError(f"Kolom target '{self.target_column}' tidak ada di dalam data.")
            
        df_work = df.copy()
        
        # Drop rows where target is NaN
        df_work = df_work.dropna(subset=[self.target_column])
        
        # Determine features
        if not self.feature_columns:
            features = [c for c in df_work.columns if c != self.target_column]
        else:
            features = [c for c in self.feature_columns if c in df_work.columns and c != self.target_column]
            
        if not features:
            raise ValueError("Tidak ada kolom fitur yang tersedia untuk melatih model.")
            
        self.training_feature_columns = features
        y_raw = df_work[self.target_column]
        X_raw = df_work[features].copy()
        
        # Detect task type
        self.task_type = detect_task_type(y_raw)
        
        # Process target
        if self.task_type == "classification":
            self.target_encoder = LabelEncoder()
            y = self.target_encoder.fit_transform(y_raw.astype(str))
            self.target_classes_ = [str(c) for c in self.target_encoder.classes_]
        else:
            y = y_raw.astype(float).values
            self.target_classes_ = None
            
        # Classify feature types
        self.numeric_cols = [c for c in features if pd.api.types.is_numeric_dtype(X_raw[c])]
        self.categorical_cols = [c for c in features if c not in self.numeric_cols]
        
        # Calculate defaults for inference fill
        for c in self.numeric_cols:
            med = float(X_raw[c].median()) if not X_raw[c].dropna().empty else 0.0
            self.numeric_medians[c] = med
            X_raw[c] = X_raw[c].fillna(med)
            
        for c in self.categorical_cols:
            mode_v = str(X_raw[c].mode().iloc[0]) if not X_raw[c].dropna().empty else "Missing"
            self.cat_modes[c] = mode_v
            X_raw[c] = X_raw[c].fillna(mode_v).astype(str)
            
        # One-hot encode categorical features
        if self.categorical_cols:
            X_encoded = pd.get_dummies(X_raw, columns=self.categorical_cols, drop_first=False)
        else:
            X_encoded = X_raw.copy()
            
        # Convert all to float/int
        X_encoded = X_encoded.astype(float)
        self.processed_feature_names = list(X_encoded.columns)
        
        # Stratify classification if possible
        stratify = None
        if self.task_type == "classification":
            counts = pd.Series(y).value_counts()
            if (counts >= 2).all() and len(counts) > 1:
                stratify = y
                
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded.values, y, 
            test_size=self.test_size, 
            random_state=self.random_state, 
            stratify=stratify
        )
        
        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "task_type": self.task_type,
            "feature_names": self.processed_feature_names,
            "target_classes": self.target_classes_,
            "original_features": self.training_feature_columns,
            "numeric_cols": self.numeric_cols,
            "categorical_cols": self.categorical_cols
        }

    def transform_single_input(self, input_dict):
        """Mengubah input dictionary tunggal menjadi vektor fitur numerik sesuai skema pelatihan."""
        row_data = {}
        for c in self.training_feature_columns:
            val = input_dict.get(c)
            if c in self.numeric_cols:
                try:
                    row_data[c] = float(val) if val is not None and val != "" else self.numeric_medians.get(c, 0.0)
                except (ValueError, TypeError):
                    row_data[c] = self.numeric_medians.get(c, 0.0)
            else:
                row_data[c] = str(val) if val is not None and val != "" else self.cat_modes.get(c, "Missing")
                
        df_row = pd.DataFrame([row_data])
        if self.categorical_cols:
            df_row = pd.get_dummies(df_row, columns=self.categorical_cols, drop_first=False)
            
        # Align with processed_feature_names
        for col in self.processed_feature_names:
            if col not in df_row.columns:
                df_row[col] = 0.0
                
        # Reorder exactly
        df_row = df_row[self.processed_feature_names].astype(float)
        return df_row.values
