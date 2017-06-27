# -*- coding:utf-8 -*-
'''
Created on 2017年3月26日

@author: hwchao
'''
from bs4 import BeautifulSoup
import re

# 按规则分割字符串 切割出需要的字符串信息 并以数组的形式返回
def txt_wrap_by(start_str, end_str, html):

        start = 0
        end = 0
        book = []
        while end != -1:
            start = html.find(start_str,start)
            start += len(start_str)
            end = html.find(end_str, start)
            if end >= 0:
                sstr = html[start:end]
                sstr = sstr.replace('\n','')
                sstr = sstr.replace('\r','')
                sstr = sstr.replace('\t','')
                sstr = sstr.replace(' ','')
#                 print sstr
                book.append(sstr)
            start = end
        return book


# 页面解析类
class HtmlParser(object):
    
    
    #解析页面，返回页面中新的url地址和页面中的数据
    def parse(self, html_cont):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont.encode("utf-8"), "html.parser", )
        informs = soup.select("#info")
        # 获取书名以及书籍图片的信息
        title_image = soup.select("#mainpic a")
        
        # 获取图书内容简介信息
        book_description = soup.select("div.related_info > div#link-report > p")
        text_content = []
        for i in book_description:
            s =  i.text
            m = s.replace("<p>", "").replace("</p>","  ")
            text_content.append(m)
        text_content = ''.join(text_content)
        print "内容简介:  "+text_content
    
        # 获取作者简介
        author = soup.select("div.related_info > div:nth-of-type(3) > div:nth-of-type(1) > div > p")
        author_content = []
        for i in author:
            s = i.text
            m = s.replace("<p>", "").replace("</p>", "  ").replace(" ", "")
            author_content.append(m)
        author_content = "".join(author_content)
        print "作者简介:  "+author_content
    
      
        # 提取书名和图片链接信息
        title = title_image[0].get("title")
        imgurl = title_image[0].get("href")
        print title,imgurl + '\n'
        
        dr = re.compile(r'<[^>]+>')
        dd = dr.sub('', str(informs[0])+"&")
#         print dd  # 输出通过标签匹配得到的源文本
        dd = dd.replace('作者:',"|").replace('出版社:',"|").replace('出版年:',"|").replace('定价:',"|").replace('装帧:',"|").replace('丛书:',"|").replace('ISBN:',"|").replace('副标题:',"|").replace('译者:',"|").replace('页数:',"|").replace('原作名:',"|").replace('&',"|")
#         print dd  # 输出替换特定文本的字符串
        book = txt_wrap_by("|","|",dd)
        return  title, imgurl, book # 返回书籍信息数组
    
    

