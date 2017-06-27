# -*- coding:utf-8 -*-
'''
Created on 2017年3月26日

@author: hwchao
'''
import urllib2


class HtmlDownloader(object):
    #加载页面，返回页面的内容
    def download(self, new_url):
        if new_url is None:
            return None
        try:
            response = urllib2.urlopen(new_url)
            if response.getcode() != 200:
                return None
            return response.read()
        except:
            return None
        

