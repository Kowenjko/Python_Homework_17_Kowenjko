

import tracemalloc
import time
import base_lib

data_url = base_lib.loadData()


def parse_ukr_net():
    ukr_data = {}
    data = []
    for i in range(len(data_url)):
        news = data_url[i].find_all('div', class_='item')
        for j in range(len(news)):
            category = {}
            category['category'] = data_url[i].find('h2').text
            category['title'] = news[j].find('a').text
            category['url'] = news[j].find('a').get('href')
            category['source'] = news[j].find('span').text[1:-1]
            category['time'] = news[j].find('time').text
            data.append(category)

    ukr_data['site'] = base_lib.SELECTED_URL
    ukr_data['news'] = data
    base_lib.write_json('news.json', ukr_data)


tracemalloc.start()
start = time.time()

parse_ukr_net()
base_lib.print_txt('Single', start)

print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
print('All done! {}'.format(time.time() - start))
