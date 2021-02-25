import re
from requests import Session
from bs4 import BeautifulSoup
import requests

def initialize(url, headers):
    sess = Session()
    res = sess.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    form_data = get_form_data(soup)
    return sess, form_data

def get_firstpage(sess, url, headers, form_data, date_filter):
    data = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$lbtnSearchFloorsheet',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': form_data['viewstate'],
            '__VIEWSTATEGENERATOR': form_data['viewgenerator'],
            '__EVENTVALIDATION': form_data['evalidation'],
            'ctl00$Hidden1': '',
            'ctl00$ASCompany$hdnAutoSuggest': '0',
            'ctl00$ASCompany$txtAutoSuggest': '',
            'ctl00$hdnNewsList': '',
            'ctl00$AutoSuggest1$hdnAutoSuggest': '0',
            'ctl00$AutoSuggest1$txtAutoSuggest': '',
            'ctl00$txtNews': '',
            'ctl00$ContentPlaceHolder1$ASCompanyFilter$hdnAutoSuggest': '0',
            'ctl00$ContentPlaceHolder1$ASCompanyFilter$txtAutoSuggest': '',
            'ctl00$ContentPlaceHolder1$txtBuyerBrokerCodeFilter': '',
            'ctl00$ContentPlaceHolder1$txtSellerBrokerCodeFilter': '',
            'ctl00$ContentPlaceHolder1$txtFloorsheetDateFilter': date_filter
        }

    try:
        res = sess.post(url, headers=headers, data=data, timeout=30)
    except:
        return None, None, None, None
    print(res, '\n')
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        total_pages = 0
        try:
            total_page_soup = soup.select_one('#ctl00_ContentPlaceHolder1_PagerControl1_litRecords')
            total_page_text = total_page_soup.get_text(strip=True)
            re_results = re.search(r'.*\[Total pages: (\d+?)]', total_page_text)
            total_pages = int(re_results.groups()[0])
        except:
            return None, None, None, None

        form_data = get_form_data(soup)
        return sess, res.text, total_pages, form_data

def get_page(sess, url, headers, data):
    # res = sess.post(url, headers=headers, data=data, timeout=30)
    res = requests.post(url, headers=headers, data=data, timeout=30)

    print(res)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        form_data = get_form_data(soup)
        return sess, res.text, form_data

def get_form_data(soup):
    form_data = {}
    form_data['viewstate'] = soup.select_one('#__VIEWSTATE')['value']
    form_data['viewgenerator'] = soup.select_one('#__VIEWSTATEGENERATOR')['value']
    form_data['evalidation'] = soup.select_one('#__EVENTVALIDATION')['value']
    return form_data

