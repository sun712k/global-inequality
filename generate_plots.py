import pandas as pd
import matplotlib.pyplot as plt
import re
import os

# Paths
base_dir = '/Users/sungeun/Documents/2021-2025 Files/[JOB] Data Analysis Portfolio/global-inequality'
data_dir = os.path.join(base_dir, 'data')
top10_path = os.path.join(data_dir, 'WID_wealth_top10.xlsx')

# Load and clean data
try:
    top_df = pd.read_excel(top10_path)
except Exception as e:
    print(f"Error loading Excel: {e}")
    exit(1)

def extract_year(col_name):
    match = re.search(r'(\d{4})$', str(col_name))
    if match:
        return match.group(1)
    else:
        return str(col_name).strip().lower()

top_df.columns = [extract_year(col) for col in top_df.columns]
if 'percentile' in top_df.columns:
    top_df.drop(columns=['percentile'], inplace=True)
top_df['country'] = top_df['country'].str.strip()

# Prepare 2024 data
top_2024 = top_df[['country', '2024']].copy()
# Convert to percentage
top_2024['2024_pct'] = top_2024['2024'] * 100

# 1. Top 5 highest share
top_5 = top_2024.sort_values('2024', ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.barh(top_5['country'], top_5['2024_pct'], color='salmon')
plt.title('Top 5 Countries with Highest Wealth Concentration (Top 10% Share, 2024)', fontsize=14)
plt.xlabel('Wealth Share of Top 10% (%)', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.xlim(0, 100)
plt.gca().invert_yaxis()
for i, v in enumerate(top_5['2024_pct']):
    plt.text(v + 1, i, f'{v:.1f}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'top_5_highest_share.png'))
plt.close()

# 2. Bottom 5 (lowest) Top 10% share
bottom_5 = top_2024.sort_values('2024', ascending=True).head(5)

plt.figure(figsize=(10, 6))
plt.barh(bottom_5['country'], bottom_5['2024_pct'], color='lightblue')
plt.title('Top 5 Countries with Lowest Wealth Concentration (Top 10% Share, 2024)', fontsize=14)
plt.xlabel('Wealth Share of Top 10% (%)', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.xlim(0, 100)
plt.gca().invert_yaxis()
for i, v in enumerate(bottom_5['2024_pct']):
    plt.text(v + 1, i, f'{v:.1f}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'bottom_5_highest_share.png'))
plt.close()

print("Images generated successfully using Matplotlib.")
