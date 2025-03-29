import pandas as pd

file_path = "../../gpu_listings.csv"
data = pd.read_csv(file_path)

def is_ti(ti_value):
    if pd.isna(ti_value):
        return ti_value

    if "not" in ti_value:
        return False
    else:
        return True

data['ti'] = data['ti'].apply(is_ti)

output_path = "../../gpu_listings.csv"
data.to_csv(output_path, index=False)
print(f"Processed data saved")