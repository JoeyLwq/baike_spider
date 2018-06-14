# baike_spider
分布式爬虫爬取百度百科词条，
将数据以html文件输出或保存到mysql数据库，
先执行node_manager.py，
后执行node_spider.py，
node_manager.py中封装url_manager_proc、result_solve_proc、store_proc三个进程，
node_spider.py中封装SpiderWork进程，
entities_manager中封装UrlManager和数据存储器，
entities_spider中封装HtmlDownloder和HtmlParser，
详细请参考流程图。
![Image text](https://github.com/JoeyLwq/baike_spider/blob/master/流程图.png)
