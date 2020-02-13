import requests
from bs4 import BeautifulSoup as bs
import csv
import time


headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

base_one_url = 'https://www.ikointl.com'
base_url = 'https://www.ikointl.com/IKO-Kite-Schools-Centers'

def generate_cat_urls():
    """Generate list of catheghorical urls"""
    url_list = []
    url_list.append(base_url)
    for i in range(1, 16):
        url_list.append(base_url+f'?page={i}')
    return url_list

def get_urls_from_cat_page(url):
    """Get urls of schools"""
    urls_list = []
    session = requests.session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        schools = soup.find_all(class_='school-public-page')
        for url in schools:
            urls_list.append(url.find('a')['href'])
        time.sleep(0.5)
    return urls_list



def get_logo_from_main(url):
    """Get urls of schools"""
    urls_list = []
    session = requests.session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        schools = soup.find_all(class_='school-public-page')
        for url in schools:
            urls_list.append(url.find('img')['src'])
        time.sleep(0.5)
    return urls_list

def get_info_from_url(url):
    """Get soome infromation from """
    list_of_url_parts = url.split('/')
    return list_of_url_parts

def get_url_ftom_part(url):
    '''makes a full url of the relative'''
    page_url = base_one_url+url
    return page_url

NA = 'NAN'
def get_school_info(url):
    """Lets parse school"""
    school_info = {}
    session = requests.session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            school_info['country_f_url'] = get_info_from_url(url)[4]
        except:
            school_info['country_f_url'] = NA
        try:
            school_info['region_f_url'] = get_info_from_url(url)[5]
        except:
            school_info['region_f_url'] = NA
        try:
            school_info['name_f_url'] = get_info_from_url(url)[6]
        except:
            school_info['name_f_url'] = NA
        school_info['name'] = soup.find('h2').text.replace('\n', '').replace(' ', '')
        school_info['img_link'] = soup.find('img', attrs={'typeof': 'foaf:Image'})['src']
        school_info['short_desc'] = soup.find('h4').text.replace('\n', '').replace(' ', '')
        school_info['add_f_desc'] = soup.find('div', class_='schooAddr').text
        school_info_agr = soup.find('div', class_='school-about-info')
        school_info['desc'] = school_info_agr.find('p', class_='school-about').text.replace('\r', '').replace('\n', '')
        school_faccil = school_info_agr.find_all('li')
        list_of_facil =[]
        for fac in school_faccil:
            list_of_facil.append(fac.text)
        school_info['faccil'] = list_of_facil
        try_map_coord = soup.find('div', id='block-block-86')
        script = try_map_coord.find_all('script')[1].text
        school_info['longit'] = script[script.find('[addr,'):script.find(']')].split(' ')[1].replace(',', '')
        school_info['latid'] = script[script.find('[addr,'):script.find(']')].split(' ')[2].replace(',', '')
        time.sleep(0.2)
        return school_info



print(get_info_from_url('https://www.ikointl.com/school/italy/reggio-calabria/new-kite-zone'))

# session = requests.session()
# request = session.get('https://www.ikointl.com/school/italy/reggio-calabria/new-kite-zone', headers=headers)
# if request.status_code == 200:
#     soup = bs(request.content, 'lxml')
#     try_map_coord = soup.find('div', id='block-block-86')
#     script = try_map_coord.find_all('script')[1].text
#     longit = script[script.find('[addr,'):script.find(']')].split(' ')[1].replace(',', '')
#     latid = script[script.find('[addr,'):script.find(']')].split(' ')[2].replace(',', '')
#     print(longit, latid)

print(get_school_info('https://www.ikointl.com/school/italy/reggio-calabria/new-kite-zone'))

