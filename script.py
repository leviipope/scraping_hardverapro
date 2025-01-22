import csv
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

def load_existing_data(csv_file):
    """
    Load existing data from the CSV file into a dictionary.
    """
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return {row["id"]: row for row in reader}
    except FileNotFoundError:
        return {}

def save_to_csv(csv_file, data, fieldnames):
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def parse_time(raw_time):
    """
    Parse the time strings like 'ma 11:38' or 'tegnap 21:53' into datetime objects.
    """
    now = datetime.now()

    if raw_time.startswith("ma"):  # "ma" = today
        time_part = raw_time.split(" ")[1]  # Extract "11:38" part
        return datetime.strptime(f"{now.strftime('%Y-%m-%d')} {time_part}", "%Y-%m-%d %H:%M")
    elif raw_time.startswith("tegnap"):  # "tegnap" = yesterday
        time_part = raw_time.split(" ")[1]  # Extract "21:53" part
        yesterday = now - timedelta(days=1)
        return datetime.strptime(f"{yesterday.strftime('%Y-%m-%d')} {time_part}", "%Y-%m-%d %H:%M")
    else:
        # Default case: parse as full date-time or date
        try:
            return datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.strptime(raw_time, "%Y-%m-%d")


# Scrape the webpage
# Initialize the iced GPU counter
iced_gpus_count = 0
iced_gpus = []

# Scrape the webpage
url = "https://hardverapro.hu/aprok/hardver/videokartya/nvidia/geforce_30xx/keres.php?stext=3080&stcid_text=&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid=&buying=0&stext_none="
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

gpu_listings = []

# File to store GPU data
csv_file = "gpu_listings.csv"
existing_data = load_existing_data(csv_file)

# Find all relevant GPU listings on the page
search_result = doc.find_all("li", class_="media")
for result in search_result:
    name = result.find("h1").a.string
    name_l = name.lower()

    str_price = result.find("span", class_="text-nowrap").string

    # Skip listings that do not match the criteria
    if str_price == "Csere" or "3080" not in name or "3070" in name or "mobile" in name_l or "hibás" in name_l:
        continue

    price = int(str_price.replace(" ", "").replace("Ft", ""))

    raw_time = result.find(class_="uad-time").time.string
    try:
        time = "Előresorolva" if raw_time is None else parse_time(raw_time)
    except Exception as e:
        print(f"Error parsing time: {raw_time}, {e}")
        continue

    iced = result.find("div", class_="uad-price").small
    iced = False if iced is None else True

    link = result.find("h1").a["href"]

    id = result["data-uadid"]

    ti = "not Ti"
    if " ti " in name_l or "3080ti" in name_l or "3080 ti" in name_l:
        ti = "Ti"

    # Check if data already exists in the CSV
    if id in existing_data:
        # Update 'iced' status if it has changed to True
        if existing_data[id]["iced"] == "False" and iced:
            existing_data[id]["iced"] = "True"
            iced_gpus_count += 1
            iced_gpus.append(f"ID: {id}, Name: {existing_data[id]['name']}")
        continue

    gpu_listings.append({
        "id": id,
        "name": name,
        "ti": ti,
        "price": price,
        "time": time,
        "iced": iced,
        "link": link,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add current date and time
    })

# Combine existing data with new data
updated_data = list(existing_data.values()) + gpu_listings

# Save the updated CSV
fieldnames = ["id", "name", "ti", "price", "time", "iced", "link", "date_added"]
save_to_csv(csv_file, updated_data, fieldnames)

# Output results
if gpu_listings:
    print(f"Added {len(gpu_listings)} new GPU listings to {csv_file}:")
    for idx, gpu in enumerate(gpu_listings, start=len(existing_data) + 1):  # Row number starts from the current count
        print(f"ID: {gpu['id']}, Name: {gpu['name']}, Price: {gpu['price']}, Row: {idx+1}, Date Added: {gpu['time']}")
else:
    print("No new GPU listings found.")

# Print iced GPU information
if iced_gpus_count > 0:
    print(f"\n{iced_gpus_count} GPU(s) got iced:")
    for gpu in iced_gpus:
        print(gpu)
else:
    print("No GPUs were iced.")