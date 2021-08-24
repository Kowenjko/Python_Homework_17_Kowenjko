"""
Розпарсити стрічку новин сайту https://www.ukr.net/ із використанням різних підходів ультизадачного програмування.

Результуючий news.JSON файл із наступною структурою:

{
    site: https://www.ukr.net/,
    news: [
            {
                category: "Економіка",
                title: "Украина купила ледокол James Clark Ross: раньше у нас не было ни одного",
                url: "https://zn.ua/ECONOMICS/ukraina-kupila-ledokol-james-clark-ross-ranshe-u-nas-ne-bylo-ni-odnoho.html",
                source: "ZN,ua",
                time: "22:12"
            },
    ]
}

"""


import tracemalloc
import time
import requests
from bs4 import BeautifulSoup
import json

SELECTED_URL = 'https://www.ukr.net'


def write_txt(adress, dictionary):
    file = open(adress, 'a')
    file.write(dictionary)
    file.close()


def loadData():
    request = requests.get(SELECTED_URL)
    soup = BeautifulSoup(request.content, 'lxml')
    return soup.find_all('section', class_="items")


def write_json(address, dictionary):
    with open(address, 'w', encoding="utf-8") as outfile:
        json.dump(dictionary, outfile, indent=4,
                  sort_keys=False, ensure_ascii=False)
        outfile.close()


def print_txt(title, start_time):
    adr = 'result.txt'
    write_txt(adr, '\n')
    write_txt(adr, '-'*50)
    write_txt(adr, f'\n{title}\n')
    write_txt(adr, '-'*50)
    write_txt(adr, "\n\tCurent %d, Peak %d" %
              tracemalloc.get_traced_memory())
    write_txt(adr, f"\n\tAll done! {format(time.time()-start_time)}")
