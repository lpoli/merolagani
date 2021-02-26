import os
import csv
from bs4 import BeautifulSoup

FIELD_NAMES = ['etrs', 'etre', 'id', 'sym', 'cid', 'tbid', 'bb', 'sb', 'p', 'v', 'amt']

def parse_dumps(folder_path):
    files = os.listdir(folder_path)
    output_filename = folder_path.split('/')[-1] + '.csv'
    with open(output_filename, 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=FIELD_NAMES, delimiter=';')
        writer.writeheader()

        # output_data = []
        for f in files:
            file_path = os.path.join(folder_path, f)
            fp = open(file_path)
            soup = BeautifulSoup(fp.read(), 'lxml')
            table_soup = soup.select_one('#ctl00_ContentPlaceHolder1_divData .table-responsive table.table tbody')

            for tr_soup in table_soup.select('tr'):
                tr_data = {
                    'etrs': '',
                    'etre': '',
                    'id': '',
                    'tbid': ''
                }
                td_data = []
                for td_soup in tr_soup.select('td'):
                    td_text = td_soup.get_text(strip=True)
                    td_data.append(td_text)
                
                tr_data['cid'] = td_data[1]
                tr_data['sym'] = td_data[2]
                tr_data['bb'] = td_data[3]
                tr_data['sb'] = td_data[4]
                tr_data['v'] = td_data[5]
                tr_data['p'] = td_data[6].replace(',', '')
                tr_data['amt'] = td_data[7].replace(',', '')
                
                # output_data.append(tr_data)
                writer.writerow(tr_data)

def parse_page(content):
    soup = BeautifulSoup(content, 'lxml')
    table_soup = soup.select_one('#ctl00_ContentPlaceHolder1_divData .table-responsive table.table tbody')

    rows = []
    for tr_soup in table_soup.select('tr'):
        tr_data = {
            'etrs': '',
            'etre': '',
            'id': '',
            'tbid': ''
        }
        td_data = []
        for td_soup in tr_soup.select('td'):
            td_text = td_soup.get_text(strip=True)
            td_data.append(td_text)
        
        tr_data['cid'] = td_data[1]
        tr_data['sym'] = td_data[2]
        tr_data['bb'] = td_data[3]
        tr_data['sb'] = td_data[4]
        tr_data['v'] = td_data[5]
        tr_data['p'] = td_data[6].replace(',', '')
        tr_data['amt'] = td_data[7].replace(',', '')
        
        rows.append(tr_data)
    
    print('total rows: {}\n'.format(len(rows)))
    
    return rows
