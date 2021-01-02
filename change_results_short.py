from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Fixing team achievements'  # Set summary

limit = -1

pages = site.pages['Template:TeamResultsPage'].embeddedin()

lmt = 0

# pages = [site.pages['Unjustified Gaming']]


def change_template():
    t = mwparserfromhell.nodes.template.Template('TeamResults')
    t.add('show', 'overviewpage')
    for template in wikitext.filter_templates():
        if template.name.matches('TeamResultsPage'):
            wikitext.replace(template, t)
    return None


for page in pages:
    if lmt == limit:
        break
    lmt += 1
    print('beginning page %s' % page.name)
    text = page.text()
    wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
    change_template()
    newtext = str(wikitext)
    if text != newtext:
        print('Saving page %s...' % page.name)
        page.save(newtext, summary=summary)
    else:
        print('Skipping page %s...' % page.name)