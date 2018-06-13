#__author: Joey
#date:    2018/6/11
import json
import hashlib
import settings
import os
#URL管理器
class UrlManager(object):
    def __init__(self):
        #创建存放进度文件的文件夹
        if not os.path.isdir(settings.progress_addr):
            os.mkdir(settings.progress_addr)
        #创建存放数据的文件夹
        if settings.save_method == 'html' and not os.path.isdir(settings.store_html_addr):
            os.mkdir(settings.store_html_addr)
        self.new_urls = self.load_progress(os.path.join(settings.progress_addr,'new_urls.txt'))
        self.old_urls = self.load_progress(os.path.join(settings.progress_addr,'old_urls.txt'))

    def load_progress(self,filename):
        try:
            file = json.load(open(filename))
            print('读取进度:',filename)
            return set(file)
        except:
            print('开始新进度:',filename)
            f = open(filename,'w')
            f.close()
        return set()

    def save_progress(self,path,data):
        json.dump(list(data),open(path,'w'))
    def new_url_size(self):
        return len(self.new_urls)
    def old_url_size(self):
        return len(self.old_urls)
    def has_new_url(self):
        return self.new_url_size() != 0
    def get_new_url(self):
        url = self.new_urls.pop()
        #加密---
        m = hashlib.md5()
        m.update(bytes(url,encoding='utf-8'))
        self.old_urls.add(m.hexdigest()[8:-8])
        #------
        return url
    def add_new_url(self,url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(bytes(url,encoding='utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)
    def add_new_urls(self,urls):
        if len(urls) == 0 or urls is None:
            return
        for i in urls:
            self.add_new_url(i)

#数据存储器,以html文件输出
import time
class DataOutput_html(object):
    def __init__(self):
        self.filepath=os.path.join(settings.store_html_addr,'baike_%s.html'%(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())))
        self.output_head()
        self.data = []
    def output_head(self):
        fout = open(self.filepath,'w',encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        fout.close()
    def store_data(self,data):
        if data is None:
            return
        self.data.append(data)
        if len(self.data)>10:
            self.output_html()
    def output_html(self):
        fout = open(self.filepath,'a',encoding='utf-8')
        for data in self.data:
            fout.write("<tr>")
            fout.write("<td>%s</td>"%data['url'])
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>%s</td>" % data['content'])
            fout.write("</tr>")
            self.data.remove(data)
        fout.close()
    def output_end(self):
        fout = open(self.filepath,'a',encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

#数据存储器，将数据保存到数据库
import pymysql
class DataOutput_database(object):
    def __init__(self,table):
        self.table = table
        self.data = []
        self.conn = pymysql.connect(host=settings.database_host,user=settings.database_user,passwd=settings.database_pwd,db=settings.database,charset='utf8')
        self.cursor = self.conn.cursor()
        print('数据库连接成功')
        sql_create = '''
                        create table if not exists %s(num int auto_increment primary key,
                        url varchar(500),title varchar(150),content varchar(1000));
                        ''' % self.table
        self.cursor.execute(sql_create)
        print('数据将存入表%s'%self.table)
    def store_data(self,data):
        if data is None:
            return
        self.data.append(data)
        if len(self.data)>10:
            for i in self.data:
                sql_insert = '''
                            insert into %s(url,title,content) values('%s','%s','%s');
                            ''' % (self.table, i['url'], i['title'], i['content'])
                try:
                    self.cursor.execute(sql_insert)
                except Exception as e:
                    print('insert error:',e)
                self.data.remove(i)
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print('数据库关闭')