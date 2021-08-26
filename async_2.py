
import asyncio
from asyncio.tasks import create_task
from os import write
import tracemalloc
import time
from typing import ClassVar
import base_lib
import requests
from bs4 import BeautifulSoup
import aiohttp
import aiofiles
import json


async def load_data():
    async with aiohttp.ClientSession() as Client:
        async with Client.get(base_lib.SELECTED_URL) as response:
            page = await response.text()
            soup = BeautifulSoup(page, 'html.parser')

            return soup.find_all('section', class_="items")


async def write_json(address, dictionary):
    async with aiofiles.open(address, mode='w', encoding="utf-8") as outfile:
        await outfile.write(json.dumps(dictionary, indent=4, sort_keys=False, ensure_ascii=False))
        outfile.close()


async def parse_ukr_net(item, data_list):

    data_url = await load_data()

    news = data_url[item].find_all('div', class_='item')
    for j in range(len(news)):
        category = {}
        category['category'] = data_url[item].find('h2').text
        category['title'] = news[j].find('a').text
        category['url'] = news[j].find('a').get('href')
        category['source'] = news[j].find('span').text[1:-1]
        category['time'] = news[j].find('time').text
        data_list.append(category)
    return data_list


async def main():
    ukr_data = {}
    data = []
    data_url = await load_data()
    tasks = [asyncio.create_task(parse_ukr_net(i, data))
             for i in range(len(data_url))]
    resultat = await asyncio.gather(*tasks)

    ukr_data['site'] = base_lib.SELECTED_URL
    ukr_data['news'] = resultat

    await write_json('news.json', ukr_data)


if __name__ == "__main__":

    tracemalloc.start()
    start = time.time()
    loop = asyncio.get_event_loop()
    asyncio.run(main())
    loop.close()
    base_lib.print_txt('Async - #3', start)

    print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
    print('All done! {}'.format(time.time() - start))
