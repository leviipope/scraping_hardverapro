from logging import NullHandler

from bs4 import BeautifulSoup
import requests, re

url = "https://hardverapro.hu/aprok/hardver/videokartya/nvidia/geforce_30xx/keres.php?stext=3080&stcid_text=&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid=&buying=0&stext_none="
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

search_result = doc.find_all("li", class_="media")

for result in search_result:
    name = result.find("h1").a.string
    name_l = name.lower()

    str_price = result.find("span", class_="text-nowrap").string

    if str_price == "Csere" or "3080" not in name or "3070" in name or "mobile" in name_l or "hibás" in name_l:
        continue

    price = int(str_price.replace(" ", "").replace("Ft", ""))

    time = result.find(class_="uad-time").time.string
    if time==None:
        print("Előresorolva")
    if time is not None:
        print(time)

    iced = result.find("div", class_="uad-price").small
    if iced == None:
        iced = False
    else:
        iced = True

    link = result.find("h1").a["href"]

    id = result["data-uadid"]

    ti = "not Ti"
    if " ti " in name_l or "3080ti" in name_l:
        ti = "Ti"

    print("iced:", iced)
    print(name)
    print(ti)
    print(price)
    print(id)
    print(link)

    print("\n---\n")