import csv
from bs4 import BeautifulSoup
import requests, re

def load_exisiting_data(csv_file):
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return {row["id"]: row for row in reader}
    except FileNotFoundError:
        return {}

def save_to_csv(csv_file, data, fieldnames):
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(data)

url = "https://hardverapro.hu/aprok/hardver/videokartya/nvidia/geforce_30xx/keres.php?stext=3080&stcid_text=&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid=&buying=0&stext_none="
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

gpu_listings = []

csv_file = "gpu_listings.csv"
existing_data = load_exisiting_data(csv_file)

search_result = doc.find_all("li", class_="media")
for result in search_result:
    name = result.find("h1").a.string
    name_l = name.lower()

    str_price = result.find("span", class_="text-nowrap").string

    if str_price == "Csere" or "3080" not in name or "3070" in name or "mobile" in name_l or "hibás" in name_l:
        continue

    price = int(str_price.replace(" ", "").replace("Ft", ""))

    time = result.find(class_="uad-time").time.string
    time = "Előresorolva" if time is None else time

    iced = result.find("div", class_="uad-price").small
    iced = False if iced is None else True

    link = result.find("h1").a["href"]

    id = result["data-uadid"]

    ti = "not Ti"
    if " ti " in name_l or "3080ti" in name_l:
        ti = "Ti"

    # Check if data already in the csv
    if id in existing_data:
        continue

    gpu_listings.append({
        "id": id,
        "name": name,
        "ti": ti,
        "price": price,
        "time": time,
        "iced": iced,
        "link": link,
    })

# Save only new data to the CSV file
fieldnames = ["id", "name", "ti", "price", "time", "iced", "link"]
if gpu_listings:  # Only write if there are new entries
    save_to_csv(csv_file, gpu_listings, fieldnames)
    print(f"Added {len(gpu_listings)} new GPU listings to {csv_file}.")
else:
    print("No new GPU listings found.")

'''
# Save data to a new CSV file
csv_file = "gpu_listings.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "ti", "price", "time", "iced", "link"])
    writer.writeheader()
    writer.writerows(gpu_listings)

print(f"Data has been saved to {csv_file}.")
'''