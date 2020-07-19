from log_into_wiki import *

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Creating bracket tooltips'  # Set summary

with open('list_of_brackets.txt', encoding="utf-8") as f:
	pages = f.readlines()

limit = -1
lmt = 0

for page in pages:
	if lmt == limit:
		break
	lmt += 1
	page = page.strip()
	site.pages['Tooltip:{}'.format(page)].save('{{BracketTooltip}}', summary=summary)
	print('Saving page %s...' % page)