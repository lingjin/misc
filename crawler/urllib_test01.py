# https://blog.csdn.net/c406495762/article/details/58716886
# -*- coding: UTF-8 -*- 
from urllib import request
import chardet

if __name__ == "__main__": 
    response = request.urlopen("http://fanyi.baidu.com") 
    html = response.read()
    charset = chardet.detect(html)
    print(charset)
