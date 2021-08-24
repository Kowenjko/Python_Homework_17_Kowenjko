
from multiprocessing import Pool
import tracemalloc
import time
import functools
import base_lib


data_url = base_lib.loadData()


def parse_ukr_net(item, data_list):
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


def smap(f):
    return f()


def main():
    ukr_data = {}
    data = []
    procs = []
    for i in range(len(data_url)):
        f_inc = functools.partial(parse_ukr_net, i, data)
        procs.append(f_inc)
    with Pool() as pool:
        data = pool.map(smap, [procs[n] for n in range(len(procs))])

    ukr_data['site'] = base_lib.SELECTED_URL
    ukr_data['news'] = data[0]
    base_lib.write_json('news.json', ukr_data)


if __name__ == "__main__":
    tracemalloc.start()
    start = time.time()

    main()
    base_lib.print_txt('Process - #1', start)

    print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
    print('All done! {}'.format(time.time() - start))
