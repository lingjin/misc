# https://www.jianshu.com/p/e597b5921112

import urllib.request
import re

if __name__ == "__main__": 
    indexUrl="http://www.shicimingju.com/book/sanguoyanyi.html"
    html = urllib.request.urlopen(indexUrl).read()
    html = html.decode('utf8')
    # print(html)
    book_name = re.findall('<h1>(.*)</h1>',html,re.S)
    chapter = re.findall('href="/book/.{0,30}\d\.html">(.*?)</a>',html,re.S)
    bookurl = re.findall('href="(/book/.{0,30}\d\.html)">',html,re.S)
    chapterUrlBegin = re.sub('.html','',indexUrl)
