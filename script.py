from logging import NullHandler

from bs4 import BeautifulSoup
import requests, re

url = "https://hardverapro.hu/aprok/hardver/videokartya/nvidia/geforce_30xx/keres.php?stext=3080&stcid_text=&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid=&buying=0&stext_none="
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

search_result = doc.find_all("li", class_="media")
for result in search_result:
    str_price = result.find("span", class_="text-nowrap").string
    if str_price == "Csere":
        continue

    name = result.find("h1").a.string
    name_l = name.lower()
    if "3080" not in name or "3070" in name or "mobile" in name_l:
        continue
    print(name)

    price = int(str_price.replace(" ", "").replace("Ft", ""))
    print(price)

    time = result.find(class_="uad-time").time.string
    if time==None:
        print("Előresorolva")
        continue
    print(time)

    iced = result.find("div", class_="uad-price").small
    if iced != None:
        iced = True
    iced = False
    print("iced:", iced)

    link = result.find("h1").a["href"]
    print(link)

    id = result["data-uadid"]
    print(id)

    ti = "not Ti"
    if " ti " in name_l or "3080ti" in name_l:
        ti = "Ti"

    print(ti)

    print("------------------")

