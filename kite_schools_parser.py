import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import random
import pandas as pd




NA = 'na'

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}



base_url = 'https://www.kite-schools.com/kiteschools/'
app_url = 'https://www.kite-schools.com'


csv_columns = ['page_url', 'country_f_url', 'region_f_url', 'name_f_url', 'continent', 'name', 'img_url', 'img_name',
               'short_desc', 'website', 'add_f_desc', 'desc', 'faccil', 'longit', 'latid']

df = pd.DataFrame(columns=csv_columns)
t_df = pd.DataFrame(columns=csv_columns)

list_of_dicts = []

def list_of_countrys_url(base_url, app_url):
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
    return url_list


url_list = list_of_countrys_url(base_url=base_url, app_url=app_url)[1:]


def save_schools_to_df(url, df, t_df):
    try:
        list_val_from_ur = url.split('/')
        session = requests.session()
        request = session.get(url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            table = soup.find('table', attrs={'style': 'kiteshopborder'})
            trs = table.find_all('tr')
            idx = 1
            for tr in trs[1:]:
                try:
                    sc_url = app_url+tr.find('a')['href']
                    df.loc[idx, 'page_url'] = sc_url
                except:
                    df.loc[idx, 'page_url'] = NA
                tds = tr.find_all('td')
                try:
                    df.loc[idx, 'country_f_url'] = tds[2].text
                except:
                    df.loc[idx, 'country_f_url'] = NA
                try:
                    df.loc[idx, 'region_f_url'] = tds[1].text
                except:
                    df.loc[idx, 'region_f_url'] = NA
                try:
                    df.loc[idx, 'continent'] = tds[1].text
                except:
                    df.loc[idx, 'continent'] = NA
                try:
                    df.loc[idx, 'name_f_url'] = tds[0].text
                except:
                    df.loc[idx, 'name_f_url'] = NA
                session = requests.session()
                request = session.get(sc_url, headers=headers)
                if request.status_code == 200:
                    soup = bs(request.content, 'lxml')
                    table = soup.find('table', class_='kitestoreborder')
                    try:
                        df.loc[idx, 'name'] = table.find('h2').text
                    except:
                        df.loc[idx, 'name'] = NA
                    try:
                        img_f = soup.find('div', id='Seite')
                        df.loc[idx, 'img_url'] = img_f.find('img')['src']
                    except:
                        df.loc[idx, 'img_url'] = NA
                    try:
                        df.loc[idx, 'img_name'] = table.find('h2').text.replace('\n', '').replace(' ', '')
                    except:
                        df.loc[idx, 'img_name'] = NA

                    try:
                        df.loc[idx, 'website'] = table.find('a').text
                    except:
                        df.loc[idx, 'website'] = NA

                frames = [t_df, df]
                t_df = pd.concat(frames)

                time.sleep(random.randrange(0.1, 1.8, 0.01))


    except:
        pass

    print(t_df)
    return t_df



for i in url_list:
    t_df = save_schools_to_df(i, df, t_df)

t_df.to_csv('kite_schools.csv')



