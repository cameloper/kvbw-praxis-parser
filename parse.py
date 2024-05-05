from bs4 import BeautifulSoup as BS
from arztsuche import *
import sys

def parse_file(path):
    with open(path, 'r') as file:
        soup = BS(file, 'lxml')
        results = soup.find_all(class_ = 'resultrow')
        for resultrow in results:
            parse_result(soup, resultrow)

def parse_result(soup, row):
    name_hours = row.find('dd', class_ = 'name')
    field = row.find('dd', class_ = 'qualifikation')
    contact = row.find('dd', class_ = 'adresse')

if __name__ == "__main__":
    file_path = sys.argv[1]
    parse_file(file_path)
