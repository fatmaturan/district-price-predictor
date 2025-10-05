import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import r2_score, mean_absolute_error
from scipy.stats import randint

# Veri yükle
df = pd.read_csv("clean_apartments1.csv")

# Model kaydetme klasörü
os.makedirs("rf_models_optimized", exist_ok=True)

# İlçeler
districts = df["district"].unique()

# Random Forest için parametre dağılımları
param_dist = {
    "n_estimators": randint(100, 300),
    "max_depth": randint(3, 20),
    "min_samples_split": randint(2, 50),
    "min_samples_leaf": randint(2, 30),
    "max_features": ["sqrt", "log2", None]
}

for dist in districts:
    print(f"\n====== {dist.upper()} ======")
    df_sub = df[df["district"] == dist]

    X = df_sub.drop(columns=["price", "district"])
    y = df_sub["price"]

    if len(df_sub) < 50:
        print(f"UYARI: {dist} ilçesinde veri çok az ({len(df_sub)} satır). Sonuçlar güvenilir olmayabilir.")
        continue

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    base_model = RandomForestRegressor(random_state=42)

    randomized = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_dist,
        n_iter=30,
        cv=3,
        scoring="r2",
        n_jobs=-1,
        random_state=42
    )

    try:
        randomized.fit(X_train, y_train)
        best_params = randomized.best_params_

        best_model = RandomForestRegressor(
            random_state=42,
            **best_params
        )
        best_model.fit(X_train, y_train)

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        r2_train = r2_score(y_train, y_train_pred)
        r2_test = r2_score(y_test, y_test_pred)
        mae_train = mean_absolute_error(y_train, y_train_pred)
        mae_test = mean_absolute_error(y_test, y_test_pred)

        print(f"R2 Train: {r2_train:.4f} | R2 Test: {r2_test:.4f}")
        print(f"MAE Train: {mae_train:,.0f} TL | MAE Test: {mae_test:,.0f} TL")
       # print(f"Seçilen Parametreler: {best_params}")

        joblib.dump(best_model, f"rf_models_optimized/model_{dist}.pkl")

    except Exception as e:
        print(f"HATA: {dist} ilçesi eğitilemedi: {e}")
