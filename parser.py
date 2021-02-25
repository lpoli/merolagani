import os
import csv
from bs4 import BeautifulSoup

def parse(folder_path):
    files = os.listdir(folder_path)
    output_filename = folder_path.split('/')[-1] + '.csv'
    with open(file_path, 'w') as fp:
        output_data = []
        for f in files:
            file_path = os.path.join(folder_path, f)
            soup = BeautifulSoup(fp.read(), 'lxml')
            table_soup = soup.select_one('#ctl00_ContentPlaceHolder1_divData .table-responsive table.table')

            for tr_soup in table_soup.select(tr):
                tr_data = []
                for td_soup in tr_soup.select(td):
                    td_text = td_soup.get_text(strip=True)
                    tr_data.append(td_text)
                
                tr_data[1:] # Don't need numbering
                output_data.append(tr_data)

    # write csv header and write output at once

            