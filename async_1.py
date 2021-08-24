
import tracemalloc
import time
import asyncio
import base_lib
from pprint import pprint

data_url = base_lib.loadData()


async def category_function(name_date, where, types):
    if types == 'text':
        result = name_date.find(where).text
    elif types == 'get':
        result = name_date.find(where).get('href')
    else:
        result = 'none'
    return result


async def parse_ukr_net():

    ukr_data = {}
    data = []

    for i in range(len(data_url)):
        news = data_url[i].find_all('div', class_='item')
        for j in range(len(news)):
            category = {}
            category['category'] = asyncio.create_task(
                category_function(data_url[i], 'h2', 'text'))
            category['title'] = asyncio.create_task(
                category_function(news[j], 'a', 'text'))
            category['url'] = asyncio.create_task(
                category_function(news[j], 'a', 'get'))
            category['source'] = asyncio.create_task(
                category_function(news[j], 'span', 'text'))
            category['time'] = asyncio.create_task(
                category_function(news[j], 'time', 'text'))
            await category['category']
            await category['title']
            await category['url']
            await category['source']
            await category['time']
            responses = await asyncio.gather(category['category'], category['title'], category['url'], category['source'], category['time'])
            pprint(responses)
            data.append(responses)

    ukr_data['site'] = base_lib.SELECTED_URL
    ukr_data['news'] = data

    base_lib.write_json('news.json', ukr_data)


if __name__ == "__main__":
    tracemalloc.start()
    start = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_ukr_net())
    loop.close()

    base_lib.print_txt('Async - #2', start)

    print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
    print('All done! {}'.format(time.time() - start))
