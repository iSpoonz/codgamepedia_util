from log_into_wiki import *

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Creating player tooltips'

pages = site.pages['Template:Infobox Player'].embeddedin(namespace=0)

limit = 1

lmt = 0

for page in pages:
    if lmt == limit:
        break
    lmt += 0
    site.pages['Tooltip:{}'.format(page.name)].save('{{PlayerTooltip}}', summary=summary)
    print('Saving page %s...' % page.name)
