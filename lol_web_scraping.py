from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time, re, codecs

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = r'C:\Users\xTeas\Downloads\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get('https://iac.leagueoflegends.com/en/country-leagues/upcoming-matches/3543973810896044032/range/0-9')

teamregex = r'(.+?) VS (.+?)$'


def check_click_exists(xpath):
    for i in range(0, 50):
        try:
            time.sleep(0.3)
            driver.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            return False


check_click_exists('//*[@id="trigger-load-more"]')

count = 0
myfile = codecs.open('scraped_matches/scraped_matchesOMA.txt', 'w', 'utf-8-sig')
for match in driver.find_elements_by_class_name('upcoming_matches.Country'):
    date_time = match.find_element_by_class_name('MatchesDate').text
    round = match.find_element_by_class_name('MatchesRound').text
    matchup = match.find_element_by_class_name('MatchesOpponents').text

    # converting from 29.05.2020 format to 2020-05-29
    date = re.findall(r'\d{2}.\d{2}.\d{4}', date_time)
    old_date_format = ''.join(date)
    datetimeobject = datetime.strptime(old_date_format, '%d.%m.%Y')
    new_date_format = datetimeobject.strftime('%Y-%m-%d')

    # converting from GMT to CET
    time = re.findall(r'(\d{1}|\d{2}):\d{2}', date_time)
    old_time = ''.join(time)
    oldtime = int(old_time) + 14
    strtime = str(oldtime) + ':00'

    match = re.match(teamregex, matchup)
    team1 = match[1]
    team2 = match[2]

    myfile.write(u'{{MatchSchedule|team1=' + team1 + ' |team2=' + team2 + ' |team1score= |team2score= |winner= |date='
                 + new_date_format + '|time=' + strtime + ' |timezone=CET |dst=yes |stream= }}' + '\n')
    count = count + 1
myfile.close()
print(count)
driver.close()
