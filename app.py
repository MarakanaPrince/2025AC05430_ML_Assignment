import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, roc_auc_score, precision_score,
    recall_score, f1_score, matthews_corrcoef,
    confusion_matrix, classification_report,
)

st.set_page_config(
    page_title="Intrusion Detection Dashboard",
    page_icon="🛰️",
    layout="wide",
)

TARGET_COL = "Target"
MODEL_DIR = "model"

st.markdown("""
<style>
    #MainMenu, footer {visibility: hidden;}
    .stApp { background: #ffffff; }
    .hero {
        background: #eaf2ff; border: 2px solid #1d4ed8; border-radius: 12px;
        padding: 26px 30px; margin-bottom: 22px;
    }
    .hero-title { font-size: 2.15rem; font-weight: 800; color: #000000; margin: 0; letter-spacing: -0.5px; }
    .hero-sub { color: #111111; font-size: 1rem; font-weight: 500; margin-top: 6px; }
    .hero-tag {
        display: inline-block; background: #15803d; color: #ffffff;
        border-radius: 20px; padding: 4px 14px; font-size: 0.8rem;
        font-weight: 700; margin-top: 12px;
    }
    section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 2px solid #000000; }
    section[data-testid="stSidebar"] * { color: #000000 !important; font-weight: 500; }
    section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 { font-weight: 800 !important; }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important; border: 2px solid #000000 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        border: 2px dashed #1d4ed8 !important; background-color: #ffffff !important;
    }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 2px solid #000000; border-left: 6px solid #1d4ed8;
        border-radius: 8px; padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] { color: #000000 !important; font-weight: 700 !important; font-size: 0.85rem; }
    div[data-testid="stMetricValue"] { color: #000000 !important; font-size: 1.7rem !important; font-weight: 800 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 2px solid #000000; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9; border: 2px solid #000000; border-bottom: none;
        border-radius: 8px 8px 0 0; color: #000000; padding: 10px 22px; font-weight: 700;
    }
    .stTabs [data-baseweb="tab"] p { color: #000000 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] { background-color: #1d4ed8 !important; }
    .stTabs [aria-selected="true"] p { color: #ffffff !important; }
    .stDataFrame { border: 2px solid #000000; border-radius: 8px; overflow: hidden; }
    h1, h2, h3, h4 { color: #000000 !important; font-weight: 800 !important; }
    p, span, label, li { color: #000000; font-weight: 500; }
    .stAlert { border: 2px solid #000000 !important; font-weight: 600; }
    code { color: #000000 !important; background-color: #f1f5f9 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    feature_names = joblib.load(f"{MODEL_DIR}/feature_names.pkl")
    models = {
        "Logistic Regression": joblib.load(f"{MODEL_DIR}/Logistic_Regression.pkl"),
        "Decision Tree": joblib.load(f"{MODEL_DIR}/Decision_Tree.pkl"),
        "kNN": joblib.load(f"{MODEL_DIR}/kNN.pkl"),
        "Naive Bayes": joblib.load(f"{MODEL_DIR}/Naive_Bayes.pkl"),
        "Random Forest": joblib.load(f"{MODEL_DIR}/Random_Forest.pkl"),
    }
    return scaler, feature_names, models


scaler, feature_names, models = load_artifacts()

#Header
st.markdown("""
<div class="hero">
    <p class="hero-title">🛰️ Network Intrusion Detection Dashboard</p>
    <p class="hero-sub">CIC-IDS-2017 · Flow-based binary classification · BENIGN vs ATTACK traffic</p>
    <span class="hero-tag">● 5 MODELS TRAINED AND READY</span>
</div>
""", unsafe_allow_html=True)

#Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Detection Console")
    uploaded_file = st.file_uploader("Upload flow-data CSV", type="csv")
    model_choice = st.selectbox("Classifier", list(models.keys()))
    st.markdown("---")

    st.markdown("### 🧭 Navigate")
    page = st.radio(
        "Choose a view",
        ["📊 Data Overview", "🎯 Model Results",  "📈 Compare All Models"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption(
        "Upload `test_data.csv`, or any CSV with the same 78 flow-based "
        "feature columns plus a `Target` column (0 = BENIGN, 1 = ATTACK).",
        text_alignment = "justify"
    )

    st.markdown("---")
    st.caption(
        "Relevance: monitoring approaches like this support intrusion "
        "detection on OT/IT-converged networks — e.g. SCADA and DCS "
        "environments where safety-critical availability depends on "
        "catching malicious traffic early.",
        text_alignment="justify"
    )
    st.markdown("---")
    st.caption("Prince A Marakana", text_alignment="center")
    st.caption("Student ID: 2025AC05430", text_alignment="center")
    st.caption("M.Tech. Artificial Intelligence/Machine Learning", text_alignment="center")

#Main page
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    missing_cols = [c for c in feature_names if c not in data.columns]

    if TARGET_COL not in data.columns:
        st.error(f"CSV must contain a '{TARGET_COL}' column (0 = BENIGN, 1 = ATTACK).")
    elif missing_cols:
        st.error(f"CSV is missing expected feature columns: {missing_cols[:5]}...")
    else:
        X = data[feature_names]
        y = data[TARGET_COL]
        X_scaled = scaler.transform(X)

        model = models[model_choice]
        preds = model.predict(X_scaled)
        proba = model.predict_proba(X_scaled)[:, 1]

        acc = accuracy_score(y, preds)
        auc = roc_auc_score(y, proba)
        prec = precision_score(y, preds)
        rec = recall_score(y, preds)
        f1 = f1_score(y, preds)
        mcc = matthews_corrcoef(y, preds)

        #Model Results
        if page == "🎯 Model Results":
            st.markdown(f"### 🎯 Evaluation — {model_choice}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Accuracy", f"{acc:.4f}")
            c2.metric("AUC Score", f"{auc:.4f}")
            c3.metric("Precision", f"{prec:.4f}")
            c4, c5, c6 = st.columns(3)
            c4.metric("Recall", f"{rec:.4f}")
            c5.metric("F1 Score", f"{f1:.4f}")
            c6.metric("MCC", f"{mcc:.4f}")

            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown("#### Classification Report")
                report = classification_report(y, preds, target_names=["BENIGN", "ATTACK"])
                st.code(report)

            with col_right:
                st.markdown("#### Confusion Matrix")
                fig, ax = plt.subplots(figsize=(2, 2))
                cm = confusion_matrix(y, preds)
                sns.heatmap(
                    cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                    xticklabels=["BENIGN", "ATTACK"],
                    yticklabels=["BENIGN", "ATTACK"],
                    cbar=False, annot_kws={"size": 14, "color": "black", "weight": "bold"},
                    linewidths=2, linecolor="black",
                )
                ax.set_xlabel("Predicted", color="black", fontsize=11, fontweight="bold")
                ax.set_ylabel("Actual", color="black", fontsize=11, fontweight="bold")
                ax.tick_params(colors="black", labelsize=10)
                for spine in ax.spines.values():
                    spine.set_edgecolor("black")
                    spine.set_linewidth(2)
                st.pyplot(fig, use_container_width=False)

        #Test data overview
        elif page == "📊 Data Overview":
            st.markdown("### 📊 Exploratory Data Analysis")

            # --- Class balance ---
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Flows", len(data))
            c2.metric("Benign Flows", int((y == 0).sum()))
            c3.metric("Attack Flows", int((y == 1).sum()))

            col_a, col_b = st.columns([1, 1])

            with col_a:
                st.markdown("#### Class Distribution")
                fig, ax = plt.subplots(figsize=(2, 2))
                counts = y.value_counts().sort_index()
                bars = ax.bar(
                    ["BENIGN", "ATTACK"], counts.values,
                    color=["#1d4ed8", "#b91c1c"], edgecolor="black", linewidth=1.5,
                )
                ax.bar_label(bars, fontsize=11, fontweight="bold", color="black")
                ax.set_ylabel("Count", fontsize=11, fontweight="bold", color="black")
                ax.tick_params(colors="black", labelsize=11)
                for spine in ax.spines.values():
                    spine.set_edgecolor("black")
                st.pyplot(fig, use_container_width=False)

            with col_b:
                st.markdown("#### Data Preview")
                st.dataframe(data.head(8), use_container_width=True)

            st.markdown("---")

            #Summary statistics
            st.markdown("#### Summary Statistics (numeric features)")
            st.dataframe(X.describe().T.style.format("{:.2f}"), use_container_width=True)

            st.markdown("---")

            #Feature distribution explorer
            st.markdown("#### Feature Distribution — BENIGN vs ATTACK")
            selected_feature = st.selectbox("Choose a feature to inspect", feature_names, index=0)

            fig, ax = plt.subplots(figsize=(8, 4))
            benign_vals = X[y == 0][selected_feature]
            attack_vals = X[y == 1][selected_feature]

            ax.hist(benign_vals, bins=30, alpha=0.6, label="BENIGN", color="#1d4ed8", edgecolor="black")
            ax.hist(attack_vals, bins=30, alpha=0.6, label="ATTACK", color="#b91c1c", edgecolor="black")
            ax.set_xlabel(selected_feature, fontsize=11, fontweight="bold", color="black")
            ax.set_ylabel("Frequency", fontsize=11, fontweight="bold", color="black")
            ax.tick_params(colors="black")
            ax.legend(frameon=True, edgecolor="black")
            for spine in ax.spines.values():
                spine.set_edgecolor("black")
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=False)

            st.markdown("---")

            #Correlation heatmap
            st.markdown("#### Feature Correlation Heatmap (top 15 by variance)")
            top_features = X.var().sort_values(ascending=False).head(15).index
            corr = X[top_features].corr()

            fig, ax = plt.subplots(figsize=(9, 7))
            sns.heatmap(
                corr, cmap="coolwarm", center=0, ax=ax,
                annot=False, linewidths=0.5, linecolor="black",
                cbar_kws={"label": "Correlation"},
            )
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8, color="black")
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8, color="black")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=False)

        #Compare All Models
        elif page == "📈 Compare All Models":
            st.markdown("### 📈 All 5 Models — Metric Comparison")
            try:
                results_df = pd.read_csv(f"{MODEL_DIR}/results_summary.csv")
                st.dataframe(
                    results_df.style.highlight_max(
                        subset=["Accuracy", "AUC", "Precision", "Recall", "F1", "MCC"],
                        color="#86efac",
                    ),
                    use_container_width=True,
                )

                metrics_to_plot = ["Accuracy", "F1", "MCC"]
                fig, ax = plt.subplots(figsize=(9, 4.5))
                x = np.arange(len(results_df["Model"]))
                width = 0.25
                colors = ["#1d4ed8", "#15803d", "#b91c1c"]

                for i, metric in enumerate(metrics_to_plot):
                    ax.bar(x + (i - 1) * width, results_df[metric], width,
                           label=metric, color=colors[i], edgecolor="black", linewidth=1.2)

                ax.set_xticks(x)
                ax.set_xticklabels(results_df["Model"], rotation=15, ha="right",
                                    fontsize=10, fontweight="bold", color="black")
                ax.set_ylabel("Score", fontsize=11, fontweight="bold", color="black")
                ax.set_ylim(0, 1.15)
                ax.tick_params(colors="black")
                ax.legend(loc="lower right", frameon=True, edgecolor="black")
                ax.set_title("Model Performance Comparison", fontsize=13, fontweight="bold", color="black")
                for spine in ax.spines.values():
                    spine.set_edgecolor("black")
                ax.grid(axis="y", linestyle="--", alpha=0.4)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=False)
            except FileNotFoundError:
                st.info("results_summary.csv not found — run train_models.py first.")

else:
    st.info("👈 Upload a flow-data CSV from the sidebar console to begin.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **What this dashboard does**
        - Loads 5 pre-trained classifiers
        - Runs predictions on uploaded flow data
        - Reports Accuracy, AUC, Precision, Recall, F1, MCC
        - Renders a confusion matrix and classification report
        """)
    with col2:
        st.markdown("""
        **Models available**
        - Logistic Regression
        - Decision Tree
        - k-Nearest Neighbors
        - Naive Bayes (Gaussian)
        - Random Forest (Ensemble)
        """)

#Footer
st.markdown("---")
st.caption(
    "This dashboard uses the **CIC-IDS-2017** dataset, made publicly available "
    "by the Canadian Institute for Cybersecurity for research and educational purposes.",
    text_alignment="justify"
)
st.caption(
    "Citation: Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani, "
    "\"Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic "
    "Characterization\", 4th International Conference on Information Systems "
    "Security and Privacy (ICISSP), Portugal, January 2018.",
    text_alignment="justify"
)