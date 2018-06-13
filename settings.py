#__author: Joey
#date:    2018/6/13
import os

#进度文件目录
progress_addr = os.path.join(os.path.abspath('.'),'progress')

#数据存储的html文件地址目录
store_html_addr = os.path.join(os.path.abspath('.'),'output_html')

#每次运行爬取的url数
crawl_num = 50

#数据存储方式 'html'以HTML文件输出数据，'database'将数据保存到mysql数据库
# save_method = 'html'
save_method = 'database'

#数据库服务器ip,用户名，密码，数据库,表
database_host = '127.0.0.1'
database_user = 'root'
database_pwd = '123456'
database = 'test'
table = 'baike'

#爬取的根url
root_url = 'https://baike.baidu.com/item/%E7%BD%91%E9%A1%B5%E6%8A%93%E5%8F%96'

