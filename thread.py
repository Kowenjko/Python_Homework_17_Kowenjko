
import tracemalloc
import threading
import time
import base_lib

data_url = base_lib.loadData()


def create_dict(data_1, data_2, data_3):
    category = {}
    category['category'] = data_1.find('h2').text
    category['title'] = data_2.find('a').text
    category['url'] = data_2.find('a').get('href')
    category['source'] = data_2.find('span').text[1:-1]
    category['time'] = data_2.find('time').text
    data_3.append(category)
    return data_3


def parse_ukr_net():
    ukr_data = {}
    data = []
    for i in range(len(data_url)):
        news = data_url[i].find_all('div', class_='item')
        threads = []
        for j in range(len(news)):
            thread = threading.Thread(
                target=create_dict, args=(data_url[i], news[j], data,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    ukr_data['site'] = base_lib.SELECTED_URL
    ukr_data['news'] = data
    base_lib.write_json('news.json', ukr_data)


if __name__ == "__main__":

    tracemalloc.start()
    start = time.time()

    parse_ukr_net()

    base_lib.print_txt('Thread - #1', start)

    print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
    print('All done! {}'.format(time.time() - start))
