"""
Project  : An Assessment of Medical Students' Adherence to Infection Prevention
           Practices during Clinical Training at Omdurman Islamic University – 2025
Script   : Data Cleaning & Recoding
Author   : Abdulrahman Sirelkhatim
Date     : January 2026
Input    : 1_data/raw/raw_data.xlsx
Output   : 1_data/cleaned/cleaned_data.xlsx
"""

import numpy as np
import pandas as pd

RAW_PATH = "1_data/raw/raw_data.xlsx"
OUTPUT_PATH = "1_data/cleaned/cleaned_data.xlsx"

LIKERT_MAP = {"Always": 5, "Often": 4, "Sometimes": 3, "Rarely": 2, "Never": 1}

ADHERENCE_COLS = [
    "wash_before",
    "wash_after",
    "alcohol_rub",
    "gloves",
    "mask",
    "sharp_disposal",
]

CORRECT_5MOMENTS = [
    "Before patient contact",
    "After patient contact",
    "After exposure to body fluids",
    "Before cleaning / aseptic procedures",
    "After touching patient surroundings",
]

TRAINING_OPTIONS = [
    "Lecture",
    "Workshop",
    "Online course",
    "Bedside teaching",
    "Others",
]

PERSONAL_BARRIERS = [
    "Lack of knowledge",
    "Forgetfulness",
    "Poor attitude",
    "Lack of experience",
]

HOSPITAL_BARRIERS = [
    "Overcrowding",
    "Lack of gloves/masks",
    "No alcohol sanitizer",
    "Poor facility hygiene",
    "Inadequate supervision",
]

INFLUENCE_OPTIONS = [
    "Training",
    "Role models",
    "Hospital environment",
    "Personal motivation",
    "Supervision",
]


def binary(val, yes_val="Yes"):
    v = str(val).strip()
    if v == yes_val:
        return 1
    if v == "No":
        return 0
    return np.nan


def recode_gender(val):
    v = str(val).strip()
    if v == "Male":
        return 1
    if v == "Female":
        return 2
    return np.nan


def recode_year(val):
    v = str(val).strip().lower()
    if "4th" in v:
        return 4
    if "5th" in v:
        return 5
    return np.nan


def clean_age(val):
    try:
        return int(str(val).strip().split()[0])
    except (ValueError, AttributeError):
        return np.nan


def recode_heard_5moments(val):
    """'Yes, No' entries (3 cases) are treated as Yes — respondent selected both options."""
    v = str(val).strip().lower()
    if "yes" in v:
        return 1
    if v == "no":
        return 0
    return np.nan


def expand_multiselect(df, raw_col, options, prefix):
    src = df[raw_col].astype(str)
    for opt in options:
        safe = opt.lower().replace(" ", "_").replace("/", "_")
        df[f"{prefix}_{safe}"] = src.apply(
            lambda x: 1
            if opt.lower() in [s.strip().lower() for s in x.split(",")]
            else 0
        )
    return df


df_raw = pd.read_excel(RAW_PATH)

df = pd.DataFrame()
df["gender"] = df_raw["Gender"].apply(recode_gender).astype("Int64")
df["age"] = df_raw["Age"].apply(clean_age).astype("Int64")
df["year_of_study"] = df_raw["Year of study "].apply(recode_year).astype("Int64")
df["ipc_training"] = (
    df_raw["Have you received formal IPC training?"].apply(binary).astype("Int64")
)
df["heard_5moments"] = (
    df_raw["Have you heard of the WHO '5 Moments for Hand Hygiene'?"]
    .apply(recode_heard_5moments)
    .astype("Int64")
)
df["know_wash_tech"] = (
    df_raw["Do yo know the correct WHO hand washing technique?"]
    .apply(binary)
    .astype("Int64")
)
df["aware_risks"] = (
    df_raw[
        "Are you aware of risks of poor IPC adherence to patients and healthcare workers?"
    ]
    .apply(binary)
    .astype("Int64")
)

for short, raw_col in zip(ADHERENCE_COLS, df_raw.columns[9:15]):
    df[short] = df_raw[raw_col].map(LIKERT_MAP).astype("Int64")

df["needle_stick"] = df_raw[df_raw.columns[15]].map(LIKERT_MAP).astype("Int64")

df["time_pressure"] = (
    df_raw[" Does time pressure affect your IPC adherence? "]
    .apply(
        lambda x: 1 if str(x).strip() == "Yes" else (0 if str(x).strip() == "No" else 2)
    )
    .astype("Int64")
)

df["staff_support"] = (
    df_raw[" Do you feel supported by hospital staff in following IPC?"]
    .apply(
        lambda x: 1 if str(x).strip() == "Yes" else (0 if str(x).strip() == "No" else 2)
    )
    .astype("Int64")
)

df["seniors_follow"] = (
    df_raw["Do senior doctors and nurses follow IPC guidelines?"]
    .map(LIKERT_MAP)
    .astype("Int64")
)

df["observation_influence"] = (
    df_raw["Does observing staff behavior influence your IPC compliance?"]
    .apply(
        lambda x: 1 if str(x).strip() == "Yes" else (0 if str(x).strip() == "No" else 2)
    )
    .astype("Int64")
)

# Training type binary dummies (col 4)
df["training_raw"] = df_raw.iloc[:, 4].astype(str)
df = expand_multiselect(df, "training_raw", TRAINING_OPTIONS, "training_type")

# 5 Moments knowledge items
df["moments_raw"] = df_raw.iloc[:, 6].astype(str)
for moment in CORRECT_5MOMENTS:
    safe = moment.lower().replace(" ", "_").replace("/", "").replace("  ", "_")
    df[f"moment_{safe}"] = df["moments_raw"].apply(
        lambda x: 1 if moment.lower() in x.lower() else 0
    )

# Personal barrier binary dummies
df["barriers_personal_raw"] = df_raw.iloc[:, 16].astype(str)
df = expand_multiselect(
    df, "barriers_personal_raw", PERSONAL_BARRIERS, "barrier_personal"
)

# Hospital barrier binary dummies
df["barriers_hospital_raw"] = df_raw.iloc[:, 17].astype(str)
df = expand_multiselect(
    df, "barriers_hospital_raw", HOSPITAL_BARRIERS, "barrier_hospital"
)

# Adherence influences binary dummies
df["influences_raw"] = df_raw.iloc[:, 22].astype(str)
df = expand_multiselect(df, "influences_raw", INFLUENCE_OPTIONS, "influence")

df.drop(
    columns=[
        "training_raw",
        "moments_raw",
        "barriers_personal_raw",
        "barriers_hospital_raw",
        "influences_raw",
    ],
    inplace=True,
)

df["knowledge_score"] = df[[c for c in df.columns if c.startswith("moment_")]].sum(
    axis=1
)

df["total_adherence_score"] = df[ADHERENCE_COLS].sum(axis=1)
df["mean_adherence_score"] = df["total_adherence_score"] / len(ADHERENCE_COLS)


def knowledge_level(score):
    if pd.isna(score):
        return pd.NA
    if score <= 2:
        return 1
    if score == 3:
        return 2
    return 3


def adherence_level(mean_score):
    if pd.isna(mean_score):
        return pd.NA
    if mean_score < 3.0:
        return 1
    if mean_score < 4.0:
        return 2
    return 3


df["knowledge_level"] = df["knowledge_score"].apply(knowledge_level).astype("Int64")
df["adherence_level"] = (
    df["mean_adherence_score"].apply(adherence_level).astype("Int64")
)
df["adherence_binary"] = (df["adherence_level"] == 3).astype("Int64")

personal_barrier_cols = [
    f"barrier_personal_{b.lower().replace(' ', '_').replace('/', '_')}"
    for b in PERSONAL_BARRIERS
]
hospital_barrier_cols = [
    f"barrier_hospital_{b.lower().replace(' ', '_').replace('/', '_')}"
    for b in HOSPITAL_BARRIERS
]
df["barriers_personal_sum"] = df[personal_barrier_cols].sum(axis=1)
df["barriers_hospital_sum"] = df[hospital_barrier_cols].sum(axis=1)
df["barriers_total"] = df["barriers_personal_sum"] + df["barriers_hospital_sum"]

influence_cols = [f"influence_{i.lower().replace(' ', '_')}" for i in INFLUENCE_OPTIONS]
df["influences_sum"] = df[influence_cols].sum(axis=1)

df.insert(0, "ID", range(1, len(df) + 1))

df.to_excel(OUTPUT_PATH, index=False)
print(f"Saved: {OUTPUT_PATH}")
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(
    f"Mean knowledge score: {df['knowledge_score'].mean():.2f} (SD={df['knowledge_score'].std():.2f})"
)
print(
    f"Mean adherence score: {df['mean_adherence_score'].mean():.2f} (SD={df['mean_adherence_score'].std():.2f})"
)
print(f"Good adherence (%): {df['adherence_binary'].mean() * 100:.1f}%")
