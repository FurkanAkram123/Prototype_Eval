import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# ====================== LOAD DATA ======================
with open('Eval_Survey_results.js', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The answers are in order - we'll create a clean DataFrame
questions = [q['text'] for q in data]
answers = [q['answers'] for q in data]          # list of 18 responses per question

df = pd.DataFrame(answers).T                    # 18 rows (participants) × 18 questions
df.columns = [f"Q{i+1}" for i in range(len(questions))]

# ====================== QUANTITATIVE SUMMARY ======================
print("=== MEAN SCORES (1-5 scale, higher = better) ===")
print(f"Prototype 1 - Forecast ease:     {pd.to_numeric(df['Q1'], errors='coerce').mean():.2f}")
print(f"Prototype 1 - Daily ranking:     {pd.to_numeric(df['Q2'], errors='coerce').mean():.2f}")
print(f"Prototype 2 - Forecast ease:     {pd.to_numeric(df['Q3'], errors='coerce').mean():.2f}")
print(f"Prototype 2 - Daily ranking:     {pd.to_numeric(df['Q4'], errors='coerce').mean():.2f}")
print(f"Prototype 3 - Forecast ease:     {pd.to_numeric(df['Q5'], errors='coerce').mean():.2f}")
print(f"Prototype 3 - Daily ranking:     {pd.to_numeric(df['Q6'], errors='coerce').mean():.2f}\n")

# Categorical counts
print("=== PREFERENCES ===")
print("Most convenient outdoor temp:", Counter(df['Q9']).most_common())
print("Most convenient energy view:  ", Counter(df['Q11']).most_common())
print("Most relevant information:    ", Counter(df['Q12']).most_common())
print("Greatest flexibility/control: ", Counter(df['Q13']).most_common())
print("Easiest during weather change:", Counter(df['Q14']).most_common())
print("Would pick prototype over own:", Counter(df['Q16']).most_common())

# ====================== SIMPLE BAR CHARTS ======================
labels = ['Proto 1', 'Proto 2', 'Proto 3']
ease_means = [
    pd.to_numeric(df['Q1'], errors='coerce').mean(),
    pd.to_numeric(df['Q3'], errors='coerce').mean(),
    pd.to_numeric(df['Q5'], errors='coerce').mean()
]
rank_means = [
    pd.to_numeric(df['Q2'], errors='coerce').mean(),
    pd.to_numeric(df['Q4'], errors='coerce').mean(),
    pd.to_numeric(df['Q6'], errors='coerce').mean()
]

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].bar(labels, ease_means, color=['#ff9999','#66b3ff','#99ff99'])
ax[0].set_title('Forecast Responsiveness Ease (higher = better)')
ax[0].set_ylim(1, 5)

ax[1].bar(labels, rank_means, color=['#ff9999','#66b3ff','#99ff99'])
ax[1].set_title('Daily Use Ranking (higher = better)')
ax[1].set_ylim(1, 5)

plt.tight_layout()
plt.show()

# ====================== SAVE SUMMARY ======================
summary = pd.DataFrame({
    'Metric': ['Forecast Ease', 'Daily Ranking'],
    'Proto 1': [ease_means[0], rank_means[0]],
    'Proto 2': [ease_means[1], rank_means[1]],
    'Proto 3': [ease_means[2], rank_means[2]]
})
summary.to_csv('prototype_evaluation_summary.csv', index=False)
print("\n✅ Summary saved to 'prototype_evaluation_summary.csv'")
print("✅ Charts displayed. Copy this script and run it!")