from log_into_wiki import *

site = login('bot', 'cod-esports')  # Set wiki

pages = [site.pages['OpTic Gaming']]

lmt = 0
for page in pages:
    text = page.text()
    print(text)