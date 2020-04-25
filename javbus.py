import re
from pyquery import PyQuery as pq#need install
from lxml import etree#need install
from bs4 import BeautifulSoup#need install
import json
from ADC_function import *
import fanza

def getActorPhoto(htmlcode): #//*[@id="star_qdt"]/li/a/img
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'star-name'})
    d={}
    for i in a:
        l=i.a['href']
        t=i.get_text()
        html = etree.fromstring(get_html(l), etree.HTMLParser())
        p=str(html.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src')).strip(" ['']")
        p2={t:p}
        d.update(p2)
    return d
def getTitle(htmlcode):  #获取标题
    doc = pq(htmlcode)
    title=str(doc('div.container h3').text()).replace(' ','-')
    try:
        title2 = re.sub('n\d+-','',title)
        return title2
    except:
        return title
def getStudio(htmlcode): #获取厂商
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[5]/a/text()')).strip(" ['']")
    return result
def getYear(htmlcode):   #获取年份
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result
def getCover(htmlcode):  #获取封面链接
    doc = pq(htmlcode)
    image = doc('a.bigImage')
    return image.attr('href')
def getRelease(htmlcode): #获取出版日期
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result
def getRuntime(htmlcode): #获取分钟
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find(text=re.compile('分鐘'))
    return a
def getActor(htmlcode):   #获取女优
    b=[]
    soup=BeautifulSoup(htmlcode,'lxml')
    a=soup.find_all(attrs={'class':'star-name'})
    for i in a:
        b.append(i.get_text())
    return b
def getNum(htmlcode):     #获取番号
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[1]/span[2]/text()')).strip(" ['']")
    return result
def getDirector(htmlcode): #获取导演
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/a/text()')).strip(" ['']")
    return result
def getCID(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    #print(htmlcode)
    string = html.xpath("//a[contains(@class,'sample-box')][1]/@href")[0].replace('https://pics.dmm.co.jp/digital/video/','')
    result = re.sub('/.*?.jpg','',string)
    return result
def getOutline(htmlcode):  #获取演员
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    try:
        result = html.xpath("string(//div[contains(@class,'mg-b20 lh4')])").replace('\n','')
        return result
    except:
        return ''
def getSerise(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[7]/a/text()')).strip(" ['']")
    return result
def getTag(htmlcode):  # 获取演员
    tag = []
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'genre'})
    for i in a:
        if 'onmouseout' in str(i):
            continue
        tag.append(i.get_text())
    return tag

def main_uncensored(number):
    htmlcode = get_html('https://www.javbus.com/' + number)
    if getTitle(htmlcode) == '':
        htmlcode = get_html('https://www.javbus.com/' + number.replace('-','_'))
    try:
        dww_htmlcode = fanza.main_htmlcode(getCID(htmlcode))
    except:
        dww_htmlcode = ''
    dic = {
        'title': str(re.sub('\w+-\d+-','',getTitle(htmlcode))).replace(getNum(htmlcode)+'-',''),
        'studio': getStudio(htmlcode),
        'year': getYear(htmlcode),
        'outline': getOutline(dww_htmlcode),
        'runtime': getRuntime(htmlcode),
        'director': getDirector(htmlcode),
        'actor': getActor(htmlcode),
        'release': getRelease(htmlcode),
        'number': getNum(htmlcode),
        'cover': getCover(htmlcode),
        'tag': getTag(htmlcode),
        'label': getSerise(htmlcode),
        'imagecut': 0,
        'actor_photo': '',
        'website': 'https://www.javbus.com/' + number,
        'source': 'javbus.py',
    }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


def main(number):
    try:
        try:
            htmlcode = get_html('https://www.javbus.com/' + number)
            try:
                dww_htmlcode = fanza.main_htmlcode(getCID(htmlcode))
            except:
                dww_htmlcode = ''
            dic = {
                'title': str(re.sub('\w+-\d+-', '', getTitle(htmlcode))),
                'studio': getStudio(htmlcode),
                'year': str(re.search('\d{4}', getYear(htmlcode)).group()),
                'outline': getOutline(dww_htmlcode),
                'runtime': getRuntime(htmlcode),
                'director': getDirector(htmlcode),
                'actor': getActor(htmlcode),
                'release': getRelease(htmlcode),
                'number': getNum(htmlcode),
                'cover': getCover(htmlcode),
                'imagecut': 1,
                'tag': getTag(htmlcode),
                'label': getSerise(htmlcode),
                'actor_photo': getActorPhoto(htmlcode),
                'website': 'https://www.javbus.com/' + number,
                'source': 'javbus.py',
            }
            js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4,
                            separators=(',', ':'), )  # .encode('UTF-8')
            return js
        except:
            return main_uncensored(number)
    except:
        data = {
            "title": "",
        }
        js = json.dumps(
            data, ensure_ascii=False, sort_keys=True, indent=4, separators=(",", ":")
        )
        return js
