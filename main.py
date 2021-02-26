import random
import time
import os
import csv
from datetime import datetime, date, timedelta
import requests
import random
from logger import get_logger
from page_loader import initialize, get_firstpage, get_page
from parser import parse_page


FIELD_NAMES = ['etrs', 'etre', 'id', 'sym', 'cid', 'tbid', 'bb', 'sb', 'p', 'v', 'amt']

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
YEAR_LIMIT = 2017
START_DATE = "12/31/2017"
OUTPUT_FOLDER = "outputs"

RANDOM_SLEEP = []
CHOICES = [1, 2, 3]
for i in range(50):
    v = random.choice(CHOICES)
    RANDOM_SLEEP.append(random.random() * v)

def random_sleep():
    time.sleep(random.choice(RANDOM_SLEEP))

if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

logger = get_logger()

start_date = datetime.strptime(START_DATE, '%m/%d/%Y')
td = 0
logger.info('Program started with start date {} and td {}'.format(START_DATE, td))


while True:
    date_filter = start_date - timedelta(td)
    if date_filter.year < YEAR_LIMIT:
        logger.info('Year limit reached')
        break

    # try: # Skip if folder already exists
    #     os.mkdir(output_folder)
    #     logger.info('{} Folder create'.format(date_filter.strftime('%Y-%m-%d')))
    # except FileExistsError:
    #     logger.debug('{} Folder exists'.format(date_filter.strftime('%Y-%m-%d')))
    #     td += 1
    #     continue
    output_path = OUTPUT_FOLDER + '/' + date_filter.strftime('%Y-%m-%d') + '.csv'

    date_filter = date_filter.strftime('%m/%d/%Y')
    logger.info('Getting data for date {}'.format(date_filter))
    logger.info('Getting new session')
    sess, form_data = initialize(URL, headers=HEADERS) # get sess object with cookies in it
    headers = HEADERS.copy()
    headers['Referer'] = URL
    headers['Origin'] = "http://merolagani.com"

    time.sleep(2)
    sess, content, total_pages, form_data = get_firstpage(sess, URL, headers=headers, form_data=form_data, date_filter=date_filter)
    if sess is None:
        td += 1
        logger.debug('No data for date {}'.format(date_filter))
        continue

    logger.info('Total pages: {}'.format(total_pages))
    file_object = open(output_path, 'w')
    writer = csv.DictWriter(file_object, fieldnames=FIELD_NAMES, delimiter=';')
    writer.writeheader()

    rows = parse_page(content)
    writer.writerows(rows)

    for i in range(2, total_pages + 1):
        logger.info('Getting page {}'.format(i))
        random_sleep()
        sess, content, form_data = get_page(sess, URL, headers, form_data=form_data, date_filter=date_filter, page_num=i)
        if sess is None:
            logger.debug('Check for page {} of date {}'.format(i, date_filter))
            sess, form_data = initialize(URL, headers=HEADERS) # Get the session back
            sess, content, total_pages, form_data = get_firstpage(sess, URL, headers=headers, form_data=form_data, date_filter=date_filter)
            if sess is None: #Break for loop and move to previous date
                td += 1
                break
            continue

        # filepath = output_folder + '/{}.html'.format(i)
        # with open(filepath, 'w') as fp:
        #     fp.write(content)
        rows = parse_page(content)
        writer.writerows(rows)

    file_object.close() # close file
    td += 1

# # parse the downloaded dumps
# folders = os.listdir(OUTPUT_FOLDER)
# for folder in folders:
#     logger.info('Parsing data for date {}'.format(folder))
#     folder_path = OUTPUT_FOLDER + '/{}'.format(folder)
#     parse(folder_path)
#     logger.info('Parsing completed for date {}'.format(folder))
