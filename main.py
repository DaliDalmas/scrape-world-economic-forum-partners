from crawler import Crawler
import time


if __name__=='__main__':
    # comment
    crawler = Crawler()
    crawler.fetch_urls()
    CONDITION = crawler.CONDITION
    while CONDITION:
        try:
            crawler.fetch_data()
        except Exception as e:
            print(e)
            print('connection stopped let sleep for a minute')
            time.sleep(60)
            try:
                crawler.fetch_data()
            except Exception as e:
                print(e)
                print('connection stopped twice let sleep for ten minutes')
                time.sleep(600)
        CONDITION = crawler.CONDITION