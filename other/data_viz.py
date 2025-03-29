import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv("../gpu_listings.csv")

# Convert 'time' and 'date_added' columns to datetime
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# 1. Price Distribution (Histogram)
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=20, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price (Ft)")
plt.ylabel("Frequency")
plt.savefig("price_distribution2025-03-29.png")  # Save plot as an image
plt.close()  # Close the plot

# 2. Price Over Time (Line Chart)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="date_added", y="price", marker="o")
plt.title("GPU Prices Over Time")
plt.xlabel("Date Added")
plt.ylabel("Price (Ft)")
plt.xticks(rotation=45)
plt.savefig("price_over_time2025-03-29.png")  # Save plot as an image
plt.close()
