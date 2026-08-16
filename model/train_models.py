import pandas as pd
import numpy as np
import joblib
import os

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score,roc_auc_score, precision_score,
                             recall_score, f1_score, matthews_corrcoef)

RANDOM_SEED = 42

train_df = pd.read_csv("train_data.csv")
test_df = pd.read_csv("../test_data.csv")

print("Train Shape: ", train_df.shape)
print("Test Shape: ", test_df.shape)

X_train = train_df.drop(columns = ["Target"])
y_train = train_df["Target"]

X_test = test_df.drop(columns = ["Target"])
y_test = test_df["Target"]

scaler = StandardScaler()
X_train_scalled = scaler.fit_transform(X_train)
X_test_scalled = scaler.transform(X_test)

models = {
    "Logistic Regression": LogisticRegression(max_iter = 1000, random_state = RANDOM_SEED),
    "Decision Tree": DecisionTreeClassifier(random_state = RANDOM_SEED),
    "kNN": KNeighborsClassifier(n_neighbors = 5),
    "Naive Bayes": GaussianNB(),
    "Random Forest": RandomForestClassifier(n_estimators = 200, random_state = RANDOM_SEED),
}

os.makedirs(".", exist_ok = True)
results = []

print(X_train.columns.tolist())

for name, model in models.items():
    model.fit(X_train_scalled, y_train)
    preds = model.predict(X_test_scalled)
    proba = model.predict_proba(X_test_scalled)[:, 1]

    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, proba)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    mcc = matthews_corrcoef(y_test, preds)

    results.append({
        "Model": name,
        "Accuracy": round(acc,4),
        "AUC": round(auc,4),
        "Precision": round(prec,4),
        "Recall": round(rec,4),
        "F1": round(f1,4),
        "MCC": round(mcc,4),
    })

    print(f"\n{name}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  AUC      : {auc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall   : {rec:.4f}")
    print(f"  F1       : {f1:.4f}")
    print(f"  MCC      : {mcc:.4f}")

    filename = name.replace(" ", "_") + ".pkl"
    joblib.dump(model, filename)

joblib.dump(scaler, "scaler.pkl")
joblib.dump(list(X_train.columns), "feature_names.pkl")

results_df = pd.DataFrame(results)
results_df.to_csv("results_summary.csv", index=False)

print("\n\n=== Summary ===")
print(results_df.to_string(index=False))
print("\nSaved 5 model .pkl files, scaler.pkl, feature_names.pkl, results_summary.csv in model/")