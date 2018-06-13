#__author: Joey
#date:    2018/6/11
from multiprocessing.managers import BaseManager
from multiprocessing import Queue
from entities_manager import UrlManager,DataOutput_html,DataOutput_database
from multiprocessing import Process
import time
import settings
import os
import sys
sys.setrecursionlimit(1000000)
# 控制调度器
# 产生并启动各进程，维护四个队列间的通信
class NodeManager(object):
    def __init__(self,url_q,result_q):
        self.url_q = url_q
        self.result_q = result_q
    def queue_task(self):
        return self.url_q
    def queue_result(self):
        return self.result_q
    def start_Manager(self):
        BaseManager.register('get_task_queue', callable=self.queue_task)
        BaseManager.register('get_result_queue', callable=self.queue_result)
        manager = BaseManager(address=('127.0.0.1', 6345), authkey=b'baike')
        return manager

    def url_manager_proc(self, url_q, conn_q, root_url):
        url_manager = UrlManager()
        init_old_url_size = url_manager.old_url_size()
        url_manager.add_new_url(root_url)
        while True:
            while (url_manager.has_new_url()):
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                # 每爬取10个url提醒一次
                old_url_size = url_manager.old_url_size()
                if (old_url_size-init_old_url_size)%10 == 0:
                    print('本次已爬取 %d urls' % (url_manager.old_url_size()-init_old_url_size))
                if (url_manager.old_url_size() > init_old_url_size+settings.crawl_num-1):
                    url_q.put('end')
                    print('通知爬行结点工作结束')
                    print('待爬取url数：',url_manager.new_url_size())
                    print('历史共已爬取url数：',url_manager.old_url_size())
                    url_manager.save_progress(os.path.join(settings.progress_addr,'new_urls.txt'), url_manager.new_urls)
                    url_manager.save_progress(os.path.join(settings.progress_addr,'old_urls.txt'), url_manager.old_urls)
                    return
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException:
                time.sleep(0.1)
    def result_solve_proc(self,result_q,conn_q,store_q):
        while True:
            if not result_q.empty():
                content = result_q.get(True)
                if content['urls'] == 'end':
                    print('收到爬虫结点的结束通知')
                    store_q.put('end')
                    return
                conn_q.put(content['urls'])
                store_q.put(content['data'])
            else:
                time.sleep(0.1)
    def store_proc(self,store_q):
        if settings.save_method == 'html':
            output = DataOutput_html()
            while True:
                if not store_q.empty():
                    data = store_q.get()
                    if data == 'end':
                        print('存储结点收到结束通知')
                        output.output_end()
                        return
                    output.store_data(data)
                else:
                    time.sleep(0.1)
        elif settings.save_method == 'database':
            output = DataOutput_database(settings.table)
            while True:
                if not store_q.empty():
                    data = store_q.get()
                    if data == 'end':
                        print('存储结点收到结束通知')
                        output.close()
                        return
                    output.store_data(data)
                else:
                    time.sleep(0.1)

if __name__ == '__main__':
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    node = NodeManager(url_q,result_q)
    manager = node.start_Manager()
    manager.start()
    root_url = settings.root_url
    url_manager_proc = Process(target=node.url_manager_proc,args=(url_q,conn_q,root_url))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q))
    result_solve_proc.daemon=True
    store_proc = Process(target=node.store_proc,args=(store_q,))
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    store_proc.join()
    manager.shutdown()
    print('连接关闭')