import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import random


NA = 'na'

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

base_url = 'https://www.kite-schools.com/kiteschools/'
app_url = 'https://www.kite-schools.com'


csv_columns = ['page_url', 'country_f_url', 'region_f_url', 'name_f_url', 'continent', 'name', 'img_url', 'img_name',
               'short_desc', 'website',
               'add_f_desc', 'desc', 'faccil', 'longit', 'latid']
list_of_dicts = []
url_list = []
session = requests.session()
request = session.get(base_url, headers=headers)
if request.status_code == 200:
    soup = bs(request.content, 'lxml')
    table = soup.find('div', id='Inhalt')
    a_s = table.find_all('a')
    for a in a_s:
        if a.text:
            url_list.append(app_url+a['href'])


no_schools_url_list = []
url_list = url_list[1:]
schools_dict = {}




for i in url_list:
    try:
        list_val_from_ur = i.split('/')
        session = requests.session()
        request = session.get(i, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            table = soup.find('table', attrs={'style': 'kiteshopborder'})
            trs = table.find_all('tr')
            for tr in trs[1:]:
                school_info = {}
                try:
                    sc_url = app_url+tr.find('a')['href']
                    school_info['page_url'] = sc_url
                except:
                    school_info['page_url'] = NA
                tds = tr.find_all('td')
                try:
                    school_info['country_f_url'] = tds[2].text
                except:
                    school_info['country_f_url'] = NA
                try:
                    school_info['region_f_url'] = tds[1].text
                except:
                    school_info['region_f_url'] = NA
                try:
                    school_info['continent'] = tds[1].text
                except:
                    school_info['continent'] = NA
                try:
                    school_info['name_f_url'] = tds[0].text
                except:
                    school_info['name_f_url'] = NA
                session = requests.session()
                request = session.get(sc_url, headers=headers)
                if request.status_code == 200:
                    soup = bs(request.content, 'lxml')
                    table = soup.find('table', class_='kitestoreborder')
                    try:
                        school_info['name'] = table.find('h2').text
                    except:
                        school_info['name'] = NA
                    try:
                        img_f = soup.find('div', id='Seite')
                        school_info['img_url'] = img_f.find('img')['src']
                    except:
                        school_info['img_url'] = NA
                    try:
                        school_info['img_name'] = table.find('h2').text.replace('\n', '').replace(' ', '')
                    except:
                        school_info['img_name'] = NA
                    school_info['short_desc'] = NA
                    school_info['add_f_desc'] = NA
                    try:
                        school_info['desc'] = table.find_all('p')[0].text
                    except:
                        school_info['desc'] = NA
                    try:
                        school_info['faccil'] = table.find_all('p')[5].text
                    except:
                        school_info['faccil'] = NA
                    try:
                        school_info['website'] = table.find('a').text
                    except:
                        school_info['website'] = NA
                    school_info['longit'] = NA
                    school_info['latid'] = NA

                # print(school_info)
                list_of_dicts.append(school_info)
                time.sleep(random.randrange(0.1, 1.8, 0.01))
                break
    except:
        pass


with open('kite-schools.csv', 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, csv_columns)
    writer.writeheader()
    for school in list_of_dicts:
        print(school)
        writer.writerow(school)


