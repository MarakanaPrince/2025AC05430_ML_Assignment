<div align="center" style="color: navy !important;">

# Machine Learning
### Assignment - 2

![BITS Pilani Logo](assets/bits_logo.png)

</div>

<div align="center" style="color: navy !important;">
<b>Prince A Marakana</b> <br>
<b>Student ID:</b> 2025AC05430<br>
M.Tech. Artificial Intelligence/Machine Learning
</div>

<div align="justify" style="color: navy !important;">

# Network Intrusion Detection (CIC-IDS-2017)

## Problem Statement
Industrial control and safety systems in the oil and gas sector — SCADA networks, DCS, and Safety Instrumented Systems (SIS) — are increasingly connected to corporate IT infrastructure, exposing them to network-based cyber threats such as DDoS and port scanning that can degrade the availability and integrity of safety-critical monitoring.This assignment addresses the underlying classification problem: given flow-level network traffic features, can a machine learning model reliably distinguish benign traffic from attack traffic in real time? Using the CIC-IDS-2017 dataset, this project implements and compares five classification algorithms to evaluate which approach offers the most reliable detection performance for this binary classification task, with an interactive Streamlit application to demonstrate model behavior on unseen test data.

## Dataset Description

- <b>Source:</b> CIC-IDS-2017 (Canadian Institute for Cybersecurity), MachineLearningCSV
- <b>Files used:</b> Monday-WorkingHours (benign traffic), Friday-Afternoon-DDoS (attack traffic)
- <b>Sampling:</b> 1000-row stratified sample — 600 BENIGN / 400 ATTACK — drawn to keep
  the assignment lightweight while preserving meaningful class balance
- <b>Features:</b> 78 flow-based features (duration, packet counts, byte rates, etc.)
- <b>Target:</b> binary — BENIGN (0) vs ATTACK (1)
- <b>Train/test split:</b> 800/200, stratified

## GitHub Repository
[Fill after seeing the results]
## Models Used

| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---|---|---|---|---|---|
| Logistic Regression | | | | | | |
| Decision Tree | | | | | | |
| kNN | | | | | | |
| Naive Bayes | | | | | | |
| Random Forest (Ensemble) | | | | | | |

## Observations

| ML Model Name | Observation about model performance |
|---|-------------------------------------|
| Logistic Regression | [Fill after seeing the results]     |
| Decision Tree |                                     |
| kNN |                                     |
| Naive Bayes |                                     |
| Random Forest (Ensemble) |                                     |
| **Overall Winner for your dataset?** | [Fill after seeing the results]     |
## Live App
[Fill after seeing the results]

</div>