import pandas as pd

# File path to the CSV file
csv_file = "../../gpu_listings.csv"  # Replace with your actual file path
output_file = "../../gpu_listings.csv"  # Output file with updated timestamps

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Function to ensure time format includes seconds
def ensure_full_timestamp(value):
    if pd.isna(value):  # Handle missing values
        return value
    if len(value) == 16:  # If format is 'yyyy-MM-dd hh:mm'
        return value + ":00"  # Add seconds
    return value  # Return unchanged if already in full format

# Apply the function to both 'time' and 'date_added' columns
if 'time' in df.columns:
    df['time'] = df['time'].apply(ensure_full_timestamp)

if 'date_added' in df.columns:
    df['date_added'] = df['date_added'].apply(ensure_full_timestamp)

# Save the updated DataFrame back to a new CSV file
df.to_csv(output_file, index=False)

print(f"Updated CSV saved to {output_file}")
