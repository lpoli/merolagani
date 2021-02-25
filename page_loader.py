import re
from requests import Session
from bs4 import BeautifulSoup

def initialize(url, headers):
    sess = Session()
    res = sess.get(url, headers=headers)
    soup = BeautifulSoup(res.text)
    form_data = get_form_data(soup)
    return sess, form_data

def get_firstpage(sess, url, headers, data):
    res = sess.post(url, headers=headers, data=data, timeout=30)
    if res.ok:
        soup = BeautifulSoup(res.text)
        total_page_soup = soup.select_one('#ctl00_ContentPlaceHolder1_PagerControl1_litRecords')
        total_page_text = total_page_soup.get_text(strip=True)
        re_results = re.search(r'.*\[Total pages: (\d+?)]', total_page_text)
        total_pages = int(re_results.groups()[0])

        form_data = get_form_data(soup)
        return sess, res.text, total_pages, form_data

def get_page(sess, url, headers, data):
    res = sess.post(url, headers=headers, data=data, timeout=30)
    if res.ok:
        soup = BeautifulSoup(res.text)
        form_data = get_form_data(soup)
        return sess, res.text, form_data

def get_form_data(soup):
    form_data = {}
    form_data['viewstate'] = soup.select_one('#__VIEWSTATE')['value']
    form_data['viewgenerator'] = soup.select_one('#__VIEWSTATEGENERATOR')['value']
    form_data['evalidation'] = soup.select_one('#__EVENTVALIDATION')['value']
    return form_data

