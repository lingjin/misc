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

    for i in range(0,len(bookurl)):
        number=re.findall('/(.{1,4})\.html',bookurl[i])
        chapterUrl=re.sub('$',"/"+number[0]+".html",chapterUrlBegin)
        chapterHtml=urllib.request.urlopen(chapterUrl).read()
        chapterHtml=chapterHtml.decode('utf-8','ignore')
        chapterText=re.findall('<div id="con2".*?>(.*?)</div>',chapterHtml,re.S)
        chapterText=re.sub('<p>','',''.join(chapterText))
        chapterText = re.sub('</p>', '', ''.join(chapterText))
        chapterText = re.sub('', ' ', ''.join(chapterText))
        f=open('.../../'+"".join(book_name)+'.txt','a',encoding='utf-8')
        f.write(chapter[i]+"\n")
        f.write(chapterText+"\n")
        f.close()
