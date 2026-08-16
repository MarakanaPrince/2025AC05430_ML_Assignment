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
Industrial control and safety systems in the oil and gas sector — SCADA networks, DCS, and Safety Instrumented Systems (SIS) — are increasingly connected to corporate IT infrastructure, exposing them to network-based cyber threats such as Web Attacks (Brute Force, XSS, SQL Injection) and port scanning that can degrade the availability and integrity of safety-critical monitoring.This assignment addresses the underlying classification problem: given flow-level network traffic features, can a machine learning model reliably distinguish benign traffic from attack traffic in real time? Using the CIC-IDS-2017 dataset, this project implements and compares five classification algorithms to evaluate which approach offers the most reliable detection performance for this binary classification task, with an interactive Streamlit application to demonstrate model behavior on unseen test data.

## Dataset Description

- <b>Source:</b> CIC-IDS-2017 (Canadian Institute for Cybersecurity), MachineLearningCSV
- <b>Files used:</b> Thursday-Morning-WebAttacks(Benign and Attack)
- <b>Sampling:</b> 1000-row stratified sample — 600 BENIGN / 400 ATTACK — drawn to keep
  the assignment lightweight while preserving meaningful class balance
- <b>Features:</b> 78 flow-based features (duration, packet counts, byte rates, etc.)
- <b>Target:</b> binary — BENIGN (0) vs ATTACK (1)
- <b>Train/test split:</b> 800/200, stratified

## GitHub Repository
[Fill after seeing the results]
## Models Used

| ML Model Name | Accuracy | AUC    | Precision | Recall | F1     | MCC    |
|---|----------|--------|-----------|--------|--------|--------|
| Logistic Regression | 0.9600   | 0.9898 | 0.9615    | 0.9375 | 0.9494 | 0.9165 |
| Decision Tree | 0.9950   | 0.9938 | 1.0000    | 0.9875 | 0.9937 | 0.9896 |
| kNN | 0.985    | 0.9953 | 0.9753    | 0.9875 | 0.9814 | 0.9689 |
| Naive Bayes | 0.9700   | 0.9789 | 0.9405    | 0.9875 | 0.9634 | 0.9388 |
| Random Forest (Ensemble) | 0.9800   | 0.9991 | 0.9750    | 0.9750 | 0.9750 | 0.9583 |

## Observations

| ML Model Name | Observation about model performance                                                                                                    |
|---|----------------------------------------------------------------------------------------------------------------------------------------|
| Logistic Regression | Trails slightly Web attack traffic patterns are likely not linearly seperable.                                                         |
| Decision Tree | Precision 1 and lower recall says its conservative ocassionally missing real attacks                                                   |
| kNN | Close to Decision Tree. Scalled flow feature separates classes                                                                         |
| Naive Bayes | Lowest precision. As features are not independent as seen in correlation matrix.                                                       |
| Random Forest (Ensemble) | Highest AUC. Shows best overall ranking and separation between classes                                                                 |
| **Overall Winner for your dataset?** | Decision Tree achieved the highest accuracy and MCC thus is the winner and Random Forest is the second as it is robut to un-seen data. |
## Live App
https://2025ac05430mlassignment2.streamlit.app/

## Dataset License & Citation

The CIC-IDS-2017 dataset consists of labeled network flows, including full 
packet payloads in pcap format, corresponding profiles, and labeled flows, 
publicly available for research use.

Citation:

> Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani, "Toward 
> Generating a New Intrusion Detection Dataset and Intrusion Traffic 
> Characterization", 4th International Conference on Information Systems 
> Security and Privacy (ICISSP), Portugal, January 2018.

Dataset source: [Canadian Institute for Cybersecurity — CIC-IDS-2017](https://www.unb.ca/cic/datasets/ids-2017.html)

</div>