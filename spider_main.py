# -*- coding:utf-8 -*-
'''
Created on 2017年3月26日

@author: hwchao
'''
import time
import url_manager, html_downloader, html_parser  # @UnresolvedImport
import random
import MySQLdb
# import re


class SpiderMain(object):
    
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
    
    def craw(self,urls,cate):
        conn = MySQLdb.connect(host = "localhost", user="hwchao", passwd="hwchao", db="book_info", port=3306, charset="utf8")
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS %s' %(cate))   #如果数据库中有的数据表则删除
        sql = """CREATE TABLE %s(
                 id int(11) NOT NULL AUTO_INCREMENT,
                                            书名  char(50),
                                            作者  char(100),
                                            副标题   varchar(50),
                                            原作品 varchar(50),
                                            出版社 varchar(50),
                                            译者  varchar(50),
                                            出版年  char(20),
                                            页数  char(5),
                                            定价 char(20),
                                            装帧 char(10),
                                            丛书  varchar(50),
                                            图片 varchar(100),
                 ISBN char(20),
                 primary key(id)
             )""" %(cate)
        cur.execute(sql)  #执行sql语句，新建一个数据表
        self.urls.add_new_urls(urls)
        i = 1
        while self.urls.has_next_url():
            time.sleep(int(format(random.randint(0, 9))))  # 设置一个随机数时间，每爬一个网页可以随机的停一段时间，防止IP被封
            new_url = self.urls.get_new_url()
            print "爬取:"+new_url + str(i)
            i = i+1
            html_cont  = self.downloader.download(new_url) # 获取网页源码
            if html_cont == None:
                continue
            title, img,book = self.parser.parse(html_cont)  # 解析页面  并返回解析出的数据
            l = len(book)
            
            # 根据返回数据的规律 对数据进行分类
            if l == 7:
                if '装' in book[5]:
                    sql = "insert into %s(作者,出版社,出版年,页数,定价,装帧,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],title,img)        
                else:
                    sql = "insert into %s(作者,出版社,出版年,定价,装帧,丛书,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],title,img)
            elif l == 8:
                if '装' in book[6]:
                    sql = "insert into %s(作者,出版社,译者,出版年,页数 ,定价 ,装帧 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],title,img)
                else:   
                    sql = "insert into %s(作者,出版社,出版年 ,页数, 定价, 装帧, 丛书 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],title,img)
            elif l== 9:
                if '装' in book[7]:
                    sql = "insert into %s(作者,出版社,原作品,译者,出版年,页数 ,定价 ,装帧 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],book[8],title,img)
                else:   
                    sql = "insert into %s(作者,出版社,译者,出版年 ,页数, 定价, 装帧, 丛书 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],book[8],title,img)
            elif l== 10:
                if '装' in book[8]:
                    sql = "insert into %s(作者,出版社,副标题,原作品,译者,出版年 ,页数, 定价, 装帧 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],book[8],book[9],title,img)                  
                else:   
                    sql = "insert into %s(作者,出版社,原作品,译者,出版年,页数 ,定价 ,装帧 ,丛书 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],book[8],book[9],title,img)
            elif l== 11:
                    sql = "insert into %s(作者,出版社,副标题,原作品,译者,出版年,页数 ,定价 ,装帧 ,丛书 ,ISBN,书名,图片) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(cate,book[0],book[1],book[2],book[3],book[4],book[5],book[6],book[7],book[8],book[9],book[10],title,img)
            cur.execute(sql)
        conn.commit()  
        print "写完成..."
        cur.close()
        conn.close() # 数据库资写入完毕
        

if __name__ == "__main__":
    conn = MySQLdb.connect(host = "localhost", user="hwchao", passwd="hwchao", db="books", port=3306, charset="utf8")
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    channel = '''小说 '''
    Categories = channel.split(',')
    start = time.clock()
    # 遍历书籍的列表
    for i in range(len(Categories)):
        urls = []
        sql = 'select burl from %s' %(Categories[i])
        cur.execute(sql)
        urlss = cur.fetchall()
        for url in urlss:
            urls.append(url['burl'])
        object_spider = SpiderMain()
        object_spider.craw(urls,Categories[i])
    end = time.clock()
    print "craw time:"+str(end-start)
    