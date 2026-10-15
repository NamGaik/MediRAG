"""
generate_chart_trajectory_example.py

Generates the trajectory prediction chart by running your ACTUAL trained
GRU model on P032's real recorded history -- not a hardcoded number.
This guarantees the chart reflects your current model's real output.

Run this from your MediRAG root folder, after phase_j_trajectory_model.py
has already trained and saved a model.

Requirements: pip install matplotlib
"""

import matplotlib.pyplot as plt

from phase_j_1_trajectory_model import load_patient_sequences, predict_next_visit

PATIENT_ID = "P032"  # ADJUST to chart a different patient
OUTPUT_PATH = "evaluation/chart_trajectory_example.png"

sequences = load_patient_sequences()
history = sequences[PATIENT_ID]

recorded_hba1c = [visit["HbA1c(%)"] for visit in history]
recent_history = history[-2:]
prediction = predict_next_visit(recent_history)
predicted_hba1c = prediction["predicted_HbA1c"]

n_recorded = len(recorded_hba1c)
x_recorded = list(range(n_recorded))
x_predicted = [n_recorded - 1, n_recorded]

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(x_recorded, recorded_hba1c, marker="o", color="#3D6B66", linewidth=2, markersize=8, label="Recorded HbA1c")
ax.plot(x_predicted, [recorded_hba1c[-1], predicted_hba1c], marker="o", color="#B98B4E",
        linewidth=2, linestyle="--", markersize=8, label="Model Prediction")
ax.scatter([n_recorded], [predicted_hba1c], color="#B98B4E", s=100, zorder=5)

labels = [f"Month {i+1}" for i in range(n_recorded)] + [f"Month {n_recorded+1}\n(Predicted)"]
ax.set_xticks(list(range(n_recorded + 1)))
ax.set_xticklabels(labels)
ax.set_ylabel("HbA1c (%)")
ax.set_title(f"Patient {PATIENT_ID}: Recorded History and Trajectory Prediction")
ax.axhline(6.5, color="gray", linestyle=":", linewidth=1, label="Diabetic threshold (6.5%)")
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=200)
print(f"Saved -> {OUTPUT_PATH}")
print(f"Recorded: {recorded_hba1c}")
print(f"Predicted next value: {predicted_hba1c}")