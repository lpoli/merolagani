import random
import time
import os
from datetime import datetime, date, timedelta
import requests
import random
from logger import get_logger
from page_loader import initialize, get_firstpage, get_page



URL = "http://merolagani.com/Floorsheet.aspx"
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
YEAR_LIMIT = 2020
START_DATE = "12/31/2020"
OUTPUT_PATH = "outputs"

RANDOM_SLEEP = []
CHOICES = [3, 4, 5]
for i in range(50):
    v = random.choice(CHOICES)
    RANDOM_SLEEP.append(random.random() * v)

def random_sleep():
    time.sleep(random.choice(RANDOM_SLEEP))

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

logger = get_logger()

start_date = datetime.strptime(START_DATE, '%m/%d/%Y')
td = 0
logger.info('Program started with start date {} and td {}'.format(start_date, td))

sess, form_data = initialize(URL, headers=HEADERS) # get sess object with cookies in it
headers = HEADERS.copy()
headers['Referer'] = URL
headers['Origin'] = "http://merolagani.com"

while True:
    date_filter = start_date - timedelta(td)
    if date_filter.year < YEAR_LIMIT:
        logger.info('Year limit reached')
        break

    output_folder = OUTPUT_PATH + '/' + date_filter.strftime('%Y-%m-%d')
    os.mkdir(output_folder)

    date_filter = date_filter.strftime('%m/%d/%Y')

    time.sleep(2)
    sess, content, total_pages, form_data = get_firstpage(sess, URL, headers=headers, form_data=form_data, date_filter=date_filter)
    if sess is None:
        td += 1
        continue
    logger.info('Total pages: {}'.format(total_pages))
    filepath = output_folder + '/1.html'
    with open(filepath, 'w') as fp:
        fp.write(content)

    for i in range(2, total_pages + 1):
        logger.info('Getting {} page'.format(i))
        random_sleep()
        data = {
            '__VIEWSTATE': form_data['viewstate'],
            '__VIEWSTATEGENERATOR': form_data['viewgenerator'],
            '__EVENTVALIDATION': form_data['evalidation'],
            # 'ctl00$Hidden1': '',
            # 'ctl00$ASCompany$hdnAutoSuggest': '0',
            # 'ctl00$ASCompany$txtAutoSuggest': '',
            # 'ctl00$hdnNewsList': '',
            # 'ctl00$AutoSuggest1$hdnAutoSuggest': '0',
            # 'ctl00$AutoSuggest1$txtAutoSuggest': '',
            # 'ctl00$txtNews': '',
            # 'ctl00$ContentPlaceHolder1$ASCompanyFilter$hdnAutoSuggest': '0',
            # 'ctl00$ContentPlaceHolder1$ASCompanyFilter$txtAutoSuggest': '',
            # 'ctl00$ContentPlaceHolder1$txtBuyerBrokerCodeFilter': '',
            # 'ctl00$ContentPlaceHolder1$txtSellerBrokerCodeFilter': '',
            # 'ctl00$ContentPlaceHolder1$txtFloorsheetDateFilter': date_filter,
            'ctl00$ContentPlaceHolder1$PagerControl1$hdnPCID': 'PC1',
            'ctl00$ContentPlaceHolder1$PagerControl1$hdnCurrentPage': i,
            'ctl00$ContentPlaceHolder1$PagerControl1$btnPaging': '',
            'ctl00$ContentPlaceHolder1$PagerControl2$hdnPCID': 'PC2',
            'ctl00$ContentPlaceHolder1$PagerControl2$hdnCurrentPage': i,
        }
        sess, content, form_data = get_page(sess, URL, headers, data=data)
        if sess is None:
            logger.debug('Check for page {} of date {}'.format(i, date_filter))
            sess, form_data = initialize(URL, headers=HEADERS) # Again get the session back
            sess, content, total_pages, form_data = get_firstpage(sess, URL, headers=headers, form_data=form_data, date_filter=date_filter)
            if sess is None: #Break for loop and move to previous date
                td += 1
                break
            continue

        filepath = output_folder + '/{}.html'.format(i)
        with open(filepath, 'w') as fp:
            fp.write(content)

    td += 1

'''
def func1():
    from requests import Session
    from bs4 import BeautifulSoup
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    url = 'http://merolagani.com/Floorsheet.aspx'
    sess = Session()
    r = sess.get(url, headers=HEADERS)
    headers = HEADERS.copy()
    headers['referer'] = url
    soup = BeautifulSoup(r.text)
    viewstate = soup.select_one('#__VIEWSTATE')['value']
    viewgenerator = soup.select_one('#__VIEWSTATEGENERATOR')['value']
    evalidation = soup.select_one('#__EVENTVALIDATION')['value']
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewgenerator,
        '__EVENTVALIDATION': evalidation,
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
        'ctl00$ContentPlaceHolder1$txtFloorsheetDateFilter': '02/02/2021',
        'ctl00$ContentPlaceHolder1$PagerControl1$hdnPCID': 'PC1',
        'ctl00$ContentPlaceHolder1$PagerControl1$hdnCurrentPage': '10',
        'ctl00$ContentPlaceHolder1$PagerControl1$btnPaging': '',
        'ctl00$ContentPlaceHolder1$PagerControl2$hdnPCID': 'PC2',
        'ctl00$ContentPlaceHolder1$PagerControl2$hdnCurrentPage': '0',
        }
    res = sess.post(url, headers=headers, data=data)
    with open('f.html', 'w') as fp:
        fp.write(res.text)
    with open('i.html', 'w') as fp:
        fp.write(r.text)
    soup = BeautifulSoup(res.text)
    viewstate = soup.select_one('#__VIEWSTATE')['value']
    viewgenerator = soup.select_one('#__VIEWSTATEGENERATOR')['value']
    evalidation = soup.select_one('#__EVENTVALIDATION')['value']
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewgenerator,
        '__EVENTVALIDATION': evalidation,
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
        'ctl00$ContentPlaceHolder1$txtFloorsheetDateFilter': '02/02/2021',
        'ctl00$ContentPlaceHolder1$PagerControl1$hdnPCID': 'PC1',
        'ctl00$ContentPlaceHolder1$PagerControl1$hdnCurrentPage': '2',
        'ctl00$ContentPlaceHolder1$PagerControl1$btnPaging': '',
        'ctl00$ContentPlaceHolder1$PagerControl2$hdnPCID': 'PC2',
        'ctl00$ContentPlaceHolder1$PagerControl2$hdnCurrentPage': '0',
        }
    res = sess.post(url, headers=headers, data=data)
    with open('h.html', 'w') as fp:
        fp.write(res.text)
'''