from bs4 import BeautifulSoup as BS
from arztsuche import *
import re

def parse_all_resultrows(html):
    arzts = list()
    soup = BS(html, 'lxml')
    results = soup.find_all(class_ = 'resultrow')
    for resultrow in results:
        arzts.append(parse_resultrow(soup, resultrow))
    return arzts

def parse_resultrow(soup, row):
    arzt = parse_arzt(row)

    praxis_dd = row.find('dd', class_ = 'adresse')
    praxis = parse_praxis(praxis_dd)
    
    detail_divs = row.find_all('div', class_ = 'column third')
    for div in detail_divs:
        for dt in div.find_all('dt'):
            if dt.string == "Schlüsselnummern:":
                ids = dict()
                dd = dt.next_sibling
                while dd is not None and dd.name == "dd":
                    id_components = dd.string.split(': ')
                    ids[id_components[0]] = id_components[1]
                    dd = dd.next_sibling
                arzt.ids = ids
            elif list(dt.stripped_strings).count('Fremdsprachen:') > 0:
                langs = list()
                dd = dt.next_sibling
                while dd is not None and dd.name == "dd":
                    langs.append(dd.string)
                    dd = dd.next_sibling
                arzt.languages = langs
            elif dt.string == "Praxisart:":
                types = list()
                dd = dt.next_sibling
                while dd is not None and dd.name == "dd":
                    types.append(dd.string)
                    dd = dd.next_sibling
                praxis.praxistypes = types
            elif dt.string == "Rechtsstatus:":
                dd = dt.next_sibling
                if dd is not None and dd.name == "dd":
                    arzt.status = dd.string
            elif dt.string == "Genehmigungen":
                permits = list()
                dd = dt.next_sibling
                while dd is not None and dd.name == "dd":
                    permits.append(dd.string)
                    dd = dd.next_sibling
                arzt.permits = permits

    arzt.praxis = praxis
    return arzt

def parse_arzt(row):
    arzt = Arzt()
    name_hours = row.find('dd', class_ = 'name')
    title_and_name = ' '.join(list(name_hours.dt.stripped_strings))
    arzt.name = title_and_name # TODO: Split this in a smart manner

    nh_dts = name_hours.find_all('dt')
    nh_dts.pop(0)

    for dt in nh_dts:
        if is_phone_table_title(dt):
            phone_table = dt.find_next_sibling('dd').table
            arzt.phone_hours = parse_hourtable(phone_table)
        if is_office_table_title(dt):
            office_table = dt.find_next_sibling('dd').table
            arzt.office_hours = parse_hourtable(office_table)

    field_focus = row.find('dd', class_ = 'qualifikation')
    bulletlist_dls = field_focus.find_all('dl', class_ = 'bulletlist')

    for dl in bulletlist_dls:
        if dl.dt.string.endswith(" / Fachgebiet"):
            field_title_string = dl.dt.string
            field_title_components = field_title_string.split(' / ')
            arzt.drtype = field_title_components[0]

            field_dds = dl.find_all('dd')
            arzt.fields = list()
            for dd in field_dds:
                arzt.fields.append(dd.string)
        elif dl.dt.string.endswith("Schwerpunkt"):
            focus_dds = dl.find_all('dd')
            arzt.focus = list()
            for dd in focus_dds:
                arzt.focus.append(dd.string)

    return arzt

def parse_praxis(dd):
    address_regex = re.compile(r'(?P<name>[\w -.]+)(?:<br/?>(?P<street_no>[\w .-]+ \d+(?:(?:-|/)\d+)?))?(?:<br/?>(?P<zip>\d{5}) (?P<city>[\w .-]+))?(?:<br/?>Ortsteil: (?P<district>[\w .-]+))?(?:<br/?>Landkreis: (?P<province>[\w .-]+))?')
    address_text = dd.p.decode_contents()
    match = address_regex.match(address_text)
    
    if not match:
        print("No match for address in text.\n{}".format(address_text))
        return None

    name = match.group('name')
    street_no = match.group('street_no')
    zip = match.group('zip')
    district = match.group('district')
    city = match.group('city')
    province = match.group('province')

    address = Address(zip, province, city, district, street_no)
    
    contact_dl = dd.dl
    if contact_dl is None:
        return Praxis(name, list(), list(), list(), list(), address)

    contact = contact_dl.dd
    links = contact.find_all('a')
    emails = list()
    weblinks = list()
    for a in links:
        if a['href'].startswith('mailto:'):
            emails.append(a.string)
        else:
            weblinks.append(a.string)

    contact_string = contact.stripped_strings
    phone_prefix = "Telefon: "
    fax_prefix = "Telefax: "
    phone_numbers = list()
    fax_numbers = list()
    for info in contact_string:
        if info.startswith(phone_prefix):
            phone_numbers.append(info.removeprefix(phone_prefix))
        elif info.startswith(fax_prefix):
            fax_numbers.append(info.removeprefix(fax_prefix))

    return Praxis(name, emails, phone_numbers, fax_numbers, weblinks, address)

def is_not_email(a):
    return not a['href'].startswith('mailto:')

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
    time_td_regex = re.compile(r'\d{2}:\d{2} - \d{2}:\d{2}')
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
            try:
                weekday = Weekday(weekday_string)
                time = Time(weekday, hours)
                days.append(time)
            except:
                print("{} is not a valid weekday value".format(weekday_string))
    return days
