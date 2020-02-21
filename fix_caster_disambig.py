from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Fixing caster links in MatchSchedule'  # Set summary

limit = -1

this_template = site.pages['Template:MatchSchedule']  # Set template
pages = this_template.embeddedin()

# pages = [site.pages['User:Ispoonz/RemoveCasterLinks']]

lmt = 0
for page in pages:
    if lmt == limit:
        break
    lmt += 1
    text = page.text()
    print('Beginning page %s' % page.name)
    wikitext = mwparserfromhell.parse(text)
    is_right_type = False
    for template in wikitext.filter_templates(recursive=False):
        if template.name.matches('MatchSchedule'):
            if template.has('pbplinks'):
                pbplinks = template.get('pbplinks').value.strip()
                template.remove('pbp')
                template.remove('pbplinks')
                template.add('pbp', str(pbplinks), before='color')
            if template.has('colorlinks'):
                colorlinks = template.get('colorlinks').value.strip()
                template.remove('color')
                template.remove('colorlinks')
                template.add('color', str(colorlinks), before='date')
    newtext = str(wikitext)
    if text != newtext:
        print('Saving page %s...' % page.name)
        page.save(newtext, summary=summary)
    else:
        print('Skipping page %s...' % page.name)