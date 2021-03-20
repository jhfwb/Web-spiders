import multiprocessing
def job():
    while True:
        print('aaaaa')
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=3)
    p1 = pool.map(target=job)

    print('111')