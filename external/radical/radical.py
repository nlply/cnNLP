# encoding=utf-8

import re
import csv
import urllib.request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup

class Radical(object):
    dictionary_filepath = 'external/radical/xinhua.csv'
    baiduhanyu_url = 'http://hanyu.baidu.com/zici/s?ptype=zici&wd=%s'

    def __init__(self):
        self.dictionary = dict()

        self.read_dictionary()
        self.origin_len = len(self.dictionary)

    def read_dictionary(self):
        file = open(self.dictionary_filepath, 'rU')
        reader = csv.reader(file)
        for line in reader:
            # self.dictionary[line[0].decode('utf-8')] = line[1].decode('utf-8')
            self.dictionary[line[0]] = line[1]
        file.close()

    # 根据self.dictionary的内容，重新写一遍本地的cvs文件
    def write_dictionary(self):
        file_obj = open(self.dictionary_filepath, 'w')
        writer = csv.writer(file_obj)
        for word in self.dictionary:
            writer.writerow([word,self.dictionary[word]])
        file_obj.close()

    def get_radical(self,word):
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            radical = self.get_radical_from_baiduhanyu(word)
            self.save()
            return radical

    def post_baidu(self,url):
        # print('url = ',url)
        url = quote(url,safe=string.printable)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            request = urllib.request.Request(url=url, headers=headers)
            # urllib.request.urlopen(url,data,timeout) :第一个参数url，第二个参数是访问url要传送的数据，第三个参数是设置超时的时间
            html = urllib.request.urlopen(request)
            html = html.read().decode('utf-8')
            # print(html)
            return html
        except Exception as e:
            print('URL Request Error:', e)
            return None

    def anlysis_radical_from_html(self,html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        li = soup.find(id="radical")
        if li==None:
            return None
        radical = li.span.contents[0]

        return radical

    def add_in_dictionary(self,word,radical):
        # add in file
        file_object = open(self.dictionary_filepath,'a+')
        file_object.write(word+','+radical+'\r\n')
        file_object.close()

        # refresh dictionary
        self.read_in_dictionary()

    def get_radical_from_baiduhanyu(self,word):
        url = self.baiduhanyu_url % word
        html = self.post_baidu(url)
        if html == None:
            return word

        radical = self.anlysis_radical_from_html(html)
        if radical == None:
            radical = word

        self.dictionary[word] = radical
        return radical


    def save(self):
        if len(self.dictionary) > self.origin_len:
            self.write_dictionary()
            self.origin_len = len(self.dictionary)

if __name__ == '__main__':
    r = Radical()
    print(r.get_radical('棶'))
    r.save()



    