from selenium import webdriver

DRIVER_PATH = r'C:\Users\xTeas\Downloads\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://iac.leagueoflegends.com/en/country-leagues/upcoming-matches/3543967453632937984/range/0-9')

# date_element = driver.find_element_by_class_name('MatchesDate')
# date = date_element.text
# print(date)

driver.find_element_by_xpath('//*[@id="trigger-load-more"]').click()

matches = []
count = 0
for match in driver.find_elements_by_class_name('upcoming_matches.Country'):
    date = match.find_element_by_xpath('//*[@id="matches-container"]/div[1]/div[2]').text
    matches.append({'date': date})
    count = count + 1
print(matches)
print(count)
driver.close()
