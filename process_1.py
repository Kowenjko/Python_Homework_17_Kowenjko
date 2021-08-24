
from multiprocessing import Manager, Process
import tracemalloc
import time
import base_lib

data_url = base_lib.loadData()


def parse_ukr_net(item, date_list):
    news = data_url[item].find_all('div', class_='item')
    for j in range(len(news)):
        category = {}
        category['category'] = data_url[item].find('h2').text
        category['title'] = news[j].find('a').text
        category['url'] = news[j].find('a').get('href')
        category['source'] = news[j].find('span').text[1:-1]
        category['time'] = news[j].find('time').text
        date_list.append(category)


def main():
    ukr_data = {}
    data = Manager().list()
    procs = []
    for i in range(len(data_url)):
        proc = Process(target=parse_ukr_net, args=(i, data))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    ukr_data['site'] = base_lib.SELECTED_URL
    ukr_data['news'] = list(data)
    base_lib.write_json('news.json', ukr_data)


if __name__ == "__main__":
    tracemalloc.start()
    start = time.time()

    main()
    base_lib.print_txt('Process - #2', start)

    print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
    print('All done! {}'.format(time.time() - start))
