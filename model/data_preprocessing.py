import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42

def clean_inf_nan(df):
    before = len(df)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    after = len(df)
    print(f"Dropped {before - after} rows")
    return df

def drop_cols(df, drop_cols):
    cols_to_drop = [c for c in drop_cols if c in df.columns]
    return df.drop(columns = cols_to_drop)

# monday = pd.read_csv("../data/Monday-WorkingHours.pcap_ISCX.csv")
thursday = pd.read_csv("../data/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv")

# print(f"Monday data shape: {monday.shape}")
print(f"Thursday data shape: {thursday.shape}")

# monday.columns = monday.columns.str.strip()
thursday.columns = thursday.columns.str.strip()

# print("Monday Labels:", monday["Label"].unique())
print("Thursday Labels:", thursday["Label"].unique())

# monday["Target"] = (monday["Label"] != "BENIGN").astype(int)
thursday["Target"] = (thursday["Label"] != "BENIGN").astype(int)

# monday = clean_inf_nan(monday)
thursday = clean_inf_nan(thursday)

drop_cls = ["Destination Port", "Flow ID", "Source IP", " Source IP", "Src IP",
             "Destination IP", " Destination IP", "Dst IP",
             "Timestamp", " Timestamp", "Label"]

# monday = drop_cols(monday, drop_cls)
thursday = drop_cols(thursday, drop_cls)

benign_sample = thursday[thursday["Target"] == 0].sample(n = 600, random_state = RANDOM_SEED)
attack_sample = thursday[thursday["Target"] == 1].sample(n = 400, random_state = RANDOM_SEED)

print("Benign sample shape:", benign_sample.shape)
print("Attack sample shape:", attack_sample.shape)
combined = pd.concat([benign_sample, attack_sample], axis=0)
combined = combined.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

print("Combined shape:", combined.shape)
print("Target value counts:\n", combined["Target"].value_counts())

train_df, test_df = train_test_split(combined, test_size = 0.2, random_state = RANDOM_SEED, stratify=combined["Target"])

print("Train shape:", train_df.shape, "\n", train_df["Target"].value_counts())
print("Test shape:", test_df.shape, "\n", test_df["Target"].value_counts())

train_df.to_csv("train_data.csv", index=False)
test_df.to_csv("../test_data.csv", index=False)

print("Saved model/train_data.csv and test_data.csv")