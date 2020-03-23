from log_into_wiki import *
import mwparserfromhell
from datetime import datetime, timedelta
from dateutil import parser

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Attempting to migrate tournament sentences to data ns'  # Set summary

limit = 1
startat_page = None
print(startat_page)

years = ['2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November',
          'December']

# pages = [
#    site.pages["TournamentsToData"]
# ]

with open("list_of_tournaments.txt") as file:
    text = file.readlines()
print('Hacking the mainframe')
wikitext = mwparserfromhell.parse(text)
for template in wikitext.filter_templates():
    print(template.name)
    if template.name.matches('NewsFree/Tournament'):
        if template.has('finished') and template.get('finished').value.strip() == 'yes':
            continue
        if template.has('date'):
            date_str = template.get('date').value.strip()
            template.remove('date')
            print(date_str)
            date = parser.parse(date_str)
            idx = (date.weekday() + 1) % 7
            sun = date - timedelta(idx)
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            data_page_name = 'Data:News/' + sun.strftime('%Y-%m-%d')
            print(data_page_name)
            data_page = site.pages[data_page_name]
            data_text = data_page.text()
            sep = '{{{{NewsData/Date|y={}|m={}|d={}}}}}\n'.format(
                date_obj.year,
                date_obj.strftime('%m'),
                date_obj.strftime('%d')
            )
            print(sep)
            data_text_tbl = data_text.split(sep)
            data_text_new = data_text_tbl[0] + sep + str(template) + '\n' + data_text_tbl[1]
            data_page.save(data_text_new, summary=summary)
            template.add('finished', 'yes')