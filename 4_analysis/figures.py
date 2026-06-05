"""
Project  : An Assessment of Medical Students' Adherence to Infection Prevention
           Practices during Clinical Training at Omdurman Islamic University – 2025
Script   : Figure Generation (all figures)
Author   : Abdulrahman Sirelkhatim
Date     : January 2026
Input    : 1_data/cleaned/cleaned_data.xlsx
Output   : 5_figures/ directory (PNG, 300 DPI)

Figures produced:
    fig01_gender_distribution.png
    fig02_year_of_study_distribution.png
    fig03_ipc_training_awareness.png
    fig04_knowledge_level_distribution.png
    fig05_five_moments_item_accuracy.png
    fig06_adherence_item_means.png
    fig07_adherence_level_distribution.png
    fig08_needle_stick_experience.png
    fig09_personal_barriers.png
    fig10_hospital_barriers.png
    fig11_adherence_influences.png
    fig12_senior_staff_ipc_compliance.png
    fig13_adherence_level_by_gender.png
    fig14_adherence_level_by_knowledge_level.png
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

DATA_PATH = "1_data/cleaned/cleaned_data.xlsx"
FIGURES_DIR = "5_figures/"

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11
plt.rcParams["figure.dpi"] = 200

BLUE = sns.color_palette("Blues_r", 6)
PALETTE = sns.color_palette("Set2")
CONTRAST = [BLUE[0], BLUE[2], BLUE[4]]


def save_fig(fig, filename):
    fig.savefig(FIGURES_DIR + filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filename}")


def remove_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def donut_pie(ax, counts, title, colors=None):
    colors = colors or PALETTE
    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors[: len(counts)],
        wedgeprops={"width": 0.6, "edgecolor": "white"},
        pctdistance=0.7,
        labeldistance=1.05,
    )
    ax.set_title(title, pad=12)


df = pd.read_excel(DATA_PATH)
n = len(df)


fig, ax = plt.subplots(figsize=(5, 5))
counts = df["gender"].map({1: "Male", 2: "Female"}).value_counts()
donut_pie(ax, counts, f"Gender Distribution (N={n})", [BLUE[1], PALETTE[1]])
save_fig(fig, "fig01_gender_distribution.png")


fig, ax = plt.subplots(figsize=(5, 5))
counts = df["year_of_study"].map({4: "4th Year", 5: "5th Year"}).value_counts()
donut_pie(ax, counts, f"Year of Study Distribution (N={n})", [BLUE[1], BLUE[3]])
save_fig(fig, "fig02_year_of_study_distribution.png")


fig, ax = plt.subplots(figsize=(7, 4))
awareness_items = {
    "Previous IPC\nTraining": "ipc_training",
    "Heard of\n5 Moments": "heard_5moments",
    "Knows Hand-\nwashing Technique": "know_wash_tech",
    "Aware of\nInfection Risks": "aware_risks",
}
yes_pcts = [(label, df[col].mean() * 100) for label, col in awareness_items.items()]
labels, vals = zip(*yes_pcts)
bars = ax.bar(labels, vals, color=BLUE[1])
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("Percentage Responding Yes (%)")
ax.set_title(f"IPC Training and Awareness (N={n})")
ax.set_ylim(0, 100)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig03_ipc_training_awareness.png")


fig, ax = plt.subplots(figsize=(6, 4))
k_order = ["Poor (0–2)", "Moderate (3)", "Good (4–5)"]
counts = df["knowledge_level"].map({1: "Poor (0–2)", 2: "Moderate (3)", 3: "Good (4–5)"}).value_counts().reindex(k_order)
pcts = counts / n * 100
bars = ax.bar(counts.index, pcts, color=CONTRAST)
for bar, v in zip(bars, pcts):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Knowledge Level")
ax.set_title(f"Knowledge Level Distribution (N={n})\nMean = 2.83 ± 1.45")
ax.set_ylim(0, 70)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig04_knowledge_level_distribution.png")


fig, ax = plt.subplots(figsize=(8, 4))
moment_cols = [c for c in df.columns if c.startswith("moment_")]
moment_labels = [
    "Before patient\ncontact",
    "After patient\ncontact",
    "After exposure\nto body fluids",
    "After touching\nsurroundings",
    "Before cleaning/\naseptic procedures",
]
moment_pcts = [df[col].mean() * 100 for col in moment_cols]
order = sorted(range(len(moment_pcts)), key=lambda i: moment_pcts[i])
sorted_labels = [moment_labels[i] for i in order]
sorted_pcts = [moment_pcts[i] for i in order]

bars = ax.barh(sorted_labels, sorted_pcts, color=BLUE[1])
for bar, v in zip(bars, sorted_pcts):
    ax.text(v + 0.5, bar.get_y() + bar.get_height() / 2, f"{v:.1f}%", va="center", fontsize=9)
ax.set_xlabel("Percentage Correctly Identified (%)")
ax.set_title(f"Correct Identification of WHO 5 Moments of Hand Hygiene (N={n})")
ax.set_xlim(0, 95)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig05_five_moments_item_accuracy.png")


fig, ax = plt.subplots(figsize=(8, 4))
adherence_labels = [
    "Wash hands\nbefore contact",
    "Wash hands\nafter contact",
    "Alcohol rub\nuse",
    "Gloves\nuse",
    "Mask\nuse",
    "Proper sharp\ndisposal",
]
adherence_cols = ["wash_before", "wash_after", "alcohol_rub", "gloves", "mask", "sharp_disposal"]
means = [df[col].mean() for col in adherence_cols]
order = sorted(range(len(means)), key=lambda i: means[i])
sorted_adh_labels = [adherence_labels[i] for i in order]
sorted_means = [means[i] for i in order]

bars = ax.barh(sorted_adh_labels, sorted_means, color=BLUE[1])
for bar, v in zip(bars, sorted_means):
    ax.text(v + 0.02, bar.get_y() + bar.get_height() / 2, f"{v:.2f}", va="center", fontsize=9)
ax.axvline(3, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax.set_xlabel("Mean Score (1–5 Likert scale)")
ax.set_title(f"IPC Practice Item Mean Scores (N={n})\nCronbach's α = 0.739")
ax.set_xlim(0, 5.5)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig06_adherence_item_means.png")


fig, ax = plt.subplots(figsize=(6, 4))
adh_order = ["Poor (<3.0)", "Moderate (3.0–3.99)", "Good (≥4.0)"]
counts = df["adherence_level"].map(
    {1: "Poor (<3.0)", 2: "Moderate (3.0–3.99)", 3: "Good (≥4.0)"}
).value_counts().reindex(adh_order)
pcts = counts / n * 100
bars = ax.bar(counts.index, pcts, color=CONTRAST)
for bar, v in zip(bars, pcts):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Adherence Level")
ax.set_title(f"IPC Adherence Level Distribution (N={n})\nMean = 3.79 ± 0.80")
ax.set_ylim(0, 65)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig07_adherence_level_distribution.png")


fig, ax = plt.subplots(figsize=(6, 4))
nsi_order = ["Never", "Rarely", "Sometimes", "Often", "Always"]
counts = df["needle_stick"].map(
    {1: "Never", 2: "Rarely", 3: "Sometimes", 4: "Often", 5: "Always"}
).value_counts().reindex(nsi_order)
pcts = counts / n * 100
bars = ax.bar(counts.index, pcts, color=BLUE[1])
for bar, v in zip(bars, pcts):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Frequency of Needle-Stick Injury")
ax.set_title(f"Needle-Stick Injury Experience During Clinical Work (N={n})")
ax.set_ylim(0, 60)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig08_needle_stick_experience.png")


fig, ax = plt.subplots(figsize=(7, 4))
p_barrier_map = {
    "barrier_personal_lack_of_knowledge": "Lack of knowledge",
    "barrier_personal_forgetfulness": "Forgetfulness",
    "barrier_personal_lack_of_experience": "Lack of experience",
    "barrier_personal_poor_attitude": "Poor attitude",
}
p_pcts = {label: df[col].mean() * 100 for col, label in p_barrier_map.items()}
p_pcts = dict(sorted(p_pcts.items(), key=lambda x: x[1]))
bars = ax.barh(list(p_pcts.keys()), list(p_pcts.values()), color=BLUE[1])
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.5, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", fontsize=9)
ax.set_xlabel("Percentage Reporting Barrier (%)")
ax.set_title(f"Personal Barriers to IPC Adherence (N={n})")
ax.set_xlim(0, 80)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig09_personal_barriers.png")


fig, ax = plt.subplots(figsize=(7, 4))
h_barrier_map = {
    "barrier_hospital_overcrowding": "Overcrowding",
    "barrier_hospital_poor_facility_hygiene": "Poor facility hygiene",
    "barrier_hospital_no_alcohol_sanitizer": "No alcohol sanitizer",
    "barrier_hospital_lack_of_gloves_masks": "Lack of gloves/masks",
    "barrier_hospital_inadequate_supervision": "Inadequate supervision",
}
h_pcts = {label: df[col].mean() * 100 for col, label in h_barrier_map.items()}
h_pcts = dict(sorted(h_pcts.items(), key=lambda x: x[1]))
bars = ax.barh(list(h_pcts.keys()), list(h_pcts.values()), color=BLUE[1])
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.5, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", fontsize=9)
ax.set_xlabel("Percentage Reporting Barrier (%)")
ax.set_title(f"Hospital-Related Barriers to IPC Adherence (N={n})")
ax.set_xlim(0, 75)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig10_hospital_barriers.png")


fig, ax = plt.subplots(figsize=(7, 4))
inf_map = {
    "influence_hospital_environment": "Hospital environment",
    "influence_training": "Training",
    "influence_personal_motivation": "Personal motivation",
    "influence_role_models": "Role models",
    "influence_supervision": "Supervision",
}
inf_pcts = {label: df[col].mean() * 100 for col, label in inf_map.items()}
inf_pcts = dict(sorted(inf_pcts.items(), key=lambda x: x[1]))
bars = ax.barh(list(inf_pcts.keys()), list(inf_pcts.values()), color=BLUE[1])
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.5, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", fontsize=9)
ax.set_xlabel("Percentage Citing as Influence (%)")
ax.set_title(f"Factors Influencing IPC Adherence (N={n})\n(Multiple responses allowed)")
ax.set_xlim(0, 85)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig11_adherence_influences.png")


fig, ax = plt.subplots(figsize=(7, 4))
freq_order = ["Never", "Rarely", "Sometimes", "Often", "Always"]
counts = df["seniors_follow"].map(
    {1: "Never", 2: "Rarely", 3: "Sometimes", 4: "Often", 5: "Always"}
).value_counts().reindex(freq_order)
pcts = counts / n * 100
bars = ax.bar(counts.index, pcts, color=BLUE[1])
for bar, v in zip(bars, pcts):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Frequency")
ax.set_title(f"Frequency of Senior Staff Following IPC Practices (N={n})")
ax.set_ylim(0, 45)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig12_senior_staff_ipc_compliance.png")


fig, ax = plt.subplots(figsize=(7, 4.5))
adh_map = {1: "Poor", 2: "Moderate", 3: "Good"}
gender_map = {1: "Male (n=83)", 2: "Female (n=73)"}
cat_labels = ["Poor", "Moderate", "Good"]
genders = [1, 2]
x = np.arange(len(gender_map))
width = 0.25

for i, cat_code in enumerate([1, 2, 3]):
    vals = []
    for g in genders:
        subset = df[df["gender"] == g]["adherence_level"]
        vals.append((subset == cat_code).mean() * 100)
    bars = ax.bar(x + i * width, vals, width, label=cat_labels[i], color=CONTRAST[i])
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"{v:.1f}%", ha="center", fontsize=8)

ax.set_xticks(x + width)
ax.set_xticklabels([gender_map[g] for g in genders])
ax.set_ylabel("Percentage (%)")
ax.set_title(f"Adherence Level by Gender (N={n})\nChi-square χ²=6.43, p=0.040")
ax.legend(title="Adherence Level", fontsize=9)
ax.set_ylim(0, 75)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig13_adherence_level_by_gender.png")


fig, ax = plt.subplots(figsize=(8, 4.5))
k_map = {1: "Poor (n=58)", 2: "Moderate (n=9)", 3: "Good (n=89)"}
k_groups = [1, 2, 3]
x = np.arange(len(k_map))

for i, cat_code in enumerate([1, 2, 3]):
    vals = []
    for k in k_groups:
        subset = df[df["knowledge_level"] == k]["adherence_level"]
        vals.append((subset == cat_code).mean() * 100)
    bars = ax.bar(x + i * width, vals, width, label=cat_labels[i], color=CONTRAST[i])
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"{v:.1f}%", ha="center", fontsize=8)

ax.set_xticks(x + width)
ax.set_xticklabels([k_map[k] for k in k_groups])
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Knowledge Level")
ax.set_title(f"Adherence Level by Knowledge Level (N={n})\nChi-square p=0.567 (not significant)")
ax.legend(title="Adherence Level", fontsize=9)
ax.set_ylim(0, 70)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig14_adherence_level_by_knowledge_level.png")

print(f"\nAll figures saved to: {FIGURES_DIR}")
