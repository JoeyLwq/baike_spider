#__author: Joey
#date:    2018/6/11
from entities_spider import HtmlDownloader,HtmlParser
from multiprocessing.managers import BaseManager
import sys
sys.setrecursionlimit(1000000)
class SpiderWork(object):
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        self.manager = BaseManager(('127.0.0.1',6345),authkey=b'baike')
        self.manager.connect()
        self.task = self.manager.get_task_queue()
        self.result = self.manager.get_result_queue()
        self.download = HtmlDownloader()
        self.parser = HtmlParser()
        print('init done')
    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    print(url)
                    if url =='end':
                        print('收到控制结点结束通知')
                        self.result.put({'urls':'end','data':'end'})
                        return
                    content = self.download.download(url)
                    urls,data = self.parser.parser(url,content)
                    self.result.put({'urls':urls,'data':data})
            except EOFError:
                return
            except Exception as e:
                print('crawl fail:',e)
if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()
