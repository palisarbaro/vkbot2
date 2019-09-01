import urllib.request
import connect
import vk
import re


def parse(html,n):
    a = html.find('бакалавров '+str(n))
    if a != -1:
        date_begin = html.find('(', a) +1
        date_end = html.find(')', date_begin)
        href = html.find('href', a)
        link_begin = html.find('"', href) + 1
        link_end = html.find('"', link_begin)

        link = html[link_begin:link_end]
        date = html[date_begin:date_end]
        reg = re.compile('[а-яА-Я]')
        date = reg.sub('', date)
        return date, link
    else:
        raise Exception("Не получается найти ссылку на странице")


def get_html():
    url = 'http://www.itmm.unn.ru/studentam/raspisanie/raspisanie-bakalavriata-i-spetsialiteta-ochnoj-formy-obucheniya/'
    resp = urllib.request.urlopen(url)
    if resp.code == 200:
        html = resp.fp.read(resp.length).decode("utf-8")
        return html
    else:
        raise Exception("Страница не доступна")


html = get_html()
for i in range(1,5):
    date, link = parse(html,i)
    print(date,link)
    db = connect.DB()
    if db.update_link(date, link,i):
        vk.send_to_all("курс %d: %s  от %s."%(i,link,date))