# -*- coding:utf-8 -*-
'''
Created on 2017年3月26日

@author: hwchao
'''


class UrlManager(object):
    
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return 
        for url in urls:
            self.new_urls.add(url)
    
    def add_new_url(self, url):
        if url is None:
            return
        self.new_urls.add(url) 
        
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def has_next_url(self):
        return len(self.new_urls) != 0
        
    
    



