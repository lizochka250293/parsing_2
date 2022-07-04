import csv
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'accept': '*/*',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.1.985 Yowser/2.5 Safa"
}
url = 'https://helix.ru/promotions'
reg = requests.get(url, headers=headers)
src = reg.text
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)

with open("index.html", encoding='utf-8') as file:
    src = file.read()
soup = BeautifulSoup(src, 'lxml')

items = soup.find_all(class_='card card-m card-border-1 full-width')
a_all = soup.find_all('a', class_='button button-secondary')
for item in a_all:
    item_url = "https://helix.ru/" + item.get('href')
    print(item_url)
print(items)

item_dict = {}
for item in items:
    item_name = item.find(class_='typography typography-paragraph typography-bold typography-headline typography-lines-3').text
    item_url = "https://helix.ru/" + item.find('a', class_='button button-secondary').get('href')
    item_dict[item_name] = item_url

with open("all_categories_dict.json", "w", encoding='utf-8') as file:
    json.dump(item_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", encoding='utf-8') as file:
    all_categories = json.load(file)
print(all_categories)
count = 0
for name, url in all_categories.items():

    reg = requests.get(url=url, headers=headers )
    src = reg.text

    with open(f"data/{count}.html", "w", encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}.html", encoding='utf-8') as file:
        src = file.read()

        soup = BeautifulSoup(src, "lxml")
        dict_item = []
        dict_all={}
        items_page = soup.find(class_="pageheader-title").text
        dict_all['категория'] = soup.find("title").text
        print(dict_all)
        items_pages = soup.find_all("table")
        total = []
        print(items_pages)
        for item in items_pages:
            it = item.find_all('p')
            for p in it[2:-2]:
                total.append(p.text)
        dict_all['отделения'] = '\n,'.join(total)
        dict_item.append(dict_all)

        with open(f'data/out{count}.csv', 'w', encoding='utf-8', newline="") as out:
            field_names = ['категория', 'отделения']
            writer = csv.DictWriter(out, field_names)
            writer.writeheader()
            for item in dict_item:
                writer.writerow(item)
    count+=1
