from bs4 import BeautifulSoup as BS
from arztsuche import *
import sys
import re

time_td_regex = re.compile(r'\d{2}:\d{2} - \d{2}:\d{2}')
phone_table_title_regex = re.compile(r'Telefonische Erreichbarkeit')
office_table_title_regex = re.compile(r'Sprechstundenzeiten')

def parse_file(path):
    with open(path, 'r') as file:
        soup = BS(file, 'lxml')
        results = soup.find_all(class_ = 'resultrow')
        for resultrow in results:
            parse_result(soup, resultrow)

def parse_result(soup, row):
    name_hours = row.find('dd', class_ = 'name')
    title_and_name = name_hours.dt.string
    nh_dts = name_hours.find_all('dt')
    nh_dts.pop(0)

    for dt in nh_dts:
        if is_phone_table_title(dt):
            phone_table = dt.find_next_sibling('dd').table
            phone_hours = parse_hourtable(phone_table)
        if is_office_table_title(dt):
            office_table = dt.find_next_sibling('dd').table
            office_hours = parse_hourtable(office_table)

    field = row.find('dd', class_ = 'qualifikation')
    contact = row.find('dd', class_ = 'adresse')

def is_phone_table_title(dt):
    dt_strings = dt.stripped_strings
    for dt_string in dt_strings:
        if dt_string == "Telefonische Erreichbarkeit":
            return True
    return False

def is_office_table_title(dt):
    dt_strings = dt.stripped_strings
    for dt_string in dt_strings:
        if dt_string == "Sprechstundenzeiten":
            return True
    return False

def parse_hourtable(table):
    days = list()
    trs = table.find_all('tr')
    for day in trs:
        hours = list()
        for time_td in day.find_all('td', string = time_td_regex):
            time_string_components = time_td.string.split(' - ')
            time_tuple = (time_string_components[0], time_string_components[1])
            hours.append(time_tuple)
        if len(hours) > 0:
            weekday_string = day.td.string[:2]
            weekday = WorkDay(weekday_string)
            time = Time(weekday, hours)
            days.append(time)
    return days

if __name__ == "__main__":
    file_path = sys.argv[1]
    parse_file(file_path)
