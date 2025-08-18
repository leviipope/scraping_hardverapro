# script.py
import csv
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from email_service import EmailService

def load_existing_data(csv_file):
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
    now = datetime.now()
    if raw_time.startswith("ma"):
        time_part = raw_time.split(" ")[1]
        return datetime.strptime(f"{now.strftime('%Y-%m-%d')} {time_part}", "%Y-%m-%d %H:%M")
    elif raw_time.startswith("tegnap"):
        time_part = raw_time.split(" ")[1]
        yesterday = now - timedelta(days=1)
        return datetime.strptime(f"{yesterday.strftime('%Y-%m-%d')} {time_part}", "%Y-%m-%d %H:%M")
    else:
        try:
            return datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.strptime(raw_time, "%Y-%m-%d")

# Load .env file if running locally
if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

# Initialize email service - can be disabled by setting to False
# You can also set an environment variable to control this
email_enabled = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "true").lower() == "true"
email_service = EmailService(enabled=email_enabled)

# Scrape the webpage
url = "https://hardverapro.hu/aprok/hardver/videokartya/nvidia/geforce_30xx/keres.php?stext=3080&stcid_text=&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid=&buying=0&stext_none="
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

gpu_listings = []
iced_gpus_count = 0
iced_gpus = []

csv_file = "gpu_listings.csv"
existing_data = load_existing_data(csv_file)

# Track IDs from the new search
new_search_ids = set()

search_result = doc.find_all("li", class_="media")
for result in search_result:
    name = result.find("h1").a.string
    name_l = name.lower()

    str_price = result.find("span", class_="text-nowrap").string

    if (str_price == "Ingyenes" or 
            str_price == "Csere" or
            "csere" in name_l or 
            "3080" not in name or 
            "3070" in name or 
            "mobile" in name_l or 
            "hibás" in name_l or 
            "keresek" in name_l):
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
    new_search_ids.add(id)

    ti = False
    if " ti " in name_l or "3080ti" in name_l or "3080 ti" in name_l:
        ti = True

    if id in existing_data:
        if existing_data[id]["iced"] == "False" and iced:
            existing_data[id]["iced"] = "True"
            iced_gpus_count += 1
            iced_gpus.append(f"ID: {id}, Name: {existing_data[id]['name']}")
        existing_data[id]["archived"] = "False"  # Ensure existing listings are marked as not archived
        continue

    gpu_listings.append({
        "id": id,
        "name": name,
        "ti": ti,
        "price": price,
        "time": time,
        "iced": iced,
        "link": link,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "archived": "False"  # New listings are not archived
    })

# Mark missing IDs as archived and print them
archived_gpus = []

for old_id in existing_data:
    if old_id not in new_search_ids and existing_data[old_id]["archived"] == "False":
        existing_data[old_id]["archived"] = "True"
        archived_gpus.append(f"ID: {old_id}, Name: {existing_data[old_id]['name']}")

# Print GPUs that got archived in this run
if archived_gpus:
    print("\nArchived GPUs:")
    for gpu in archived_gpus:
        print(gpu)
else:
    print("\nNo GPUs were archived.")

# Combine existing data with new listings
updated_data = list(existing_data.values()) + gpu_listings

# Save the updated CSV
fieldnames = ["id", "name", "ti", "price", "time", "iced", "link", "date_added", "archived"]
save_to_csv(csv_file, updated_data, fieldnames)

# Output results
if gpu_listings:
    print(f"Added {len(gpu_listings)} new GPU listings to {csv_file}:")
    for idx, gpu in enumerate(gpu_listings, start=len(existing_data) + 1):
        print(f"ID: {gpu['id']}, Name: {gpu['name']}, Price: {gpu['price']}, Row: {idx+1}, Date Added: {gpu['time']}")
else:
    print("\nNo new GPU listings found.")

if iced_gpus_count > 0:
    print(f"\n{iced_gpus_count} GPU(s) got iced:")
    for gpu in iced_gpus:
        print(gpu)
else:
    print("\nNo GPUs were iced.")

# Send emails for affordable GPUs
if gpu_listings:
    for gpu in gpu_listings:
        if gpu["price"] < 160000:
            email_service.send_email(gpu)