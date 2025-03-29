import pandas as pd

# Load the data from paste.txt
file_path = "../../gpu_listings.csv"
data = pd.read_csv(file_path)

# Fixed date for 'ma' and 'tegnap'
fixed_date = "2025-01-14"


# Function to process the 'time' column
def process_time(time_value):
    if pd.isna(time_value):  # If the time value is empty, return as is
        return time_value

    if "ma" in time_value or "tegnap" in time_value:  # Replace 'ma' or 'tegnap' with the fixed date
        time_part = time_value.split(" ")[1]
        return f"{fixed_date} {time_part}"

    elif len(time_value) == 10:  # If only a date is present (e.g., '2025-01-20')
        return f"{time_value} 12:00"

    else:  # Return other values unchanged (already have full datetime)
        return time_value


# Apply the function to the 'time' column
data['time'] = data['time'].apply(process_time)

# Save the processed data back to a new file or overwrite existing one
output_file_path = "../../gpu_listings.csv"
data.to_csv(output_file_path, index=False)

print(f"Processed data saved to {output_file_path}")
