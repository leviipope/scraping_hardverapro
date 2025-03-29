import pandas as pd

file_path = "../../gpu_listings.csv"
data = pd.read_csv(file_path)

def add(date_added_value):
    if pd.isna(date_added_value):
        return "2025-01-14 12:00"
    elif date_added_value:
        return date_added_value


data['date_added'] = data['date_added'].apply(add)

output_path = "../../gpu_listings.csv"
data.to_csv(output_path, index=False)
print(f"Processed data saved")