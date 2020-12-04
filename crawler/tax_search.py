import urllib.request
import re

def main(): 
    indexUrl="http://www.tax.lakecountyil.gov/datalets/datalet.aspx?mode=appeal_hist&UseSearch=no&pin=1528307015"
    html = urllib.request.urlopen(indexUrl).read()
    html = html.decode('utf8')
    # print(html)
    y2020_appealed = re.findall('''<td valign='top' align='left' bgColor='#ffffc9' nowrap  class="DataletData">2020</td><td valign='top' align='left' bgColor='#ffffc9' nowrap  class="DataletData">C - COM</td>''',html,re.S)
    isEmpty = (len(y2020_appealed) == 0)

    if isEmpty:
        print("Set is empty")
    else:
        print("Set is not empty")



if __name__ == '__main__':
    main()