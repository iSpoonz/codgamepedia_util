from log_into_wiki import *
import mwparserfromhell, re

site = login('bot', 'cod-esports')   # Set wiki
summary = 'Converting old tournament results templates to new'  # Set summary

limit = 1

# pages = site.pages['Template:Infobox Tournament'].embeddedin(namespace=0)

# https://regex101.com/r/HN75H4/2/
regex = r"\$(?: |)(.+?) {{Abbr\|(.+?)\|(?:.+?):(?:<ref>\[(.+?) (.+?)\] ?(?: *\- *)?''(.+?)''(?:| )</ref>|)\n"

lmt = 0
pages = [site.pages['User:Ispoonz/Regex Test']]


def process_start():
    match = re.search(regex, text)
    print(match)
    if match:
        totalprize = match[1]
        prizeunit = match[2]
        if match[4] != '' and match[4] is not None:
            ref_link = match[4]
            ref_title = match[5]
            ref_desc = match[6]
        for template in wikitext.filter_templates():
            if template.name.matches('TournamentResultsStart'):
                template.name = 'TournamentResults'
                if template.has('pointstitle'):
                    pointstitle = template.get('pointstitle')
                    template.add('points', 'yes')
                if template.has('noprize'):
                    noprize = template.get('noprize')
                    template.remove('noprize')
                if template.has('noteams'):
                    noteams = template.get('noteams')
                    template.remove('noteams')
                if totalprize != '' and prizeunit != '':
                    template.add('prize', 'yes')
                    template.add('prizeunit', prizeunit)
                    template.add('totalprize', totalprize)
                return template
    return None


def process_line():
    template.name = 'TournamentResults/Line'
    if template.has('prizeunit'):
        template.remove('prizeunit')
    if template.has('sameplaces'):
        template.remove('sameplaces')
    i = 1
    p = {}
    r = {}
    print(i)
    while template.has('p' + str(i)):
        if template.has('p' + str(i) + 'link'):
            p["player{0}".format(i)] = template.get('p' + str(i) + 'link').value.strip()
            template.remove('p' + str(i))
            template.remove('p' + str(i) + 'link')
        else:
            p["player{0}".format(i)] = template.get('p' + str(i)).value.strip()
            template.remove('p' + str(i))
        if template.has('p' + str(i) + 'role'):
            r["role{0}".format(i)] = template.get('p' + str(i) + 'role').value.strip()
            template.remove('p' + str(i) + 'role')
        else:
            r["role{0}".format(i)] = ''
        i += 1
    print(p)
    print(r)

    playerlist = ''
    for x in range(1, len(p)):
        t = mwparserfromhell.nodes.template.Template('TeamRoster/Line')
        t.add('player', p["player{0}".format(x)])
        if r["role{0}".format(x)] != '':
            t.add('role', r["role{0}".format(x)])
        t = '|' + str(t)
        playerlist += str(t)

    team = template.get('team').value.strip()
    template.remove('team')
    template.add('team', team + ' ' + playerlist)
    print(playerlist)
    return template


for page in pages:
    if lmt == limit:
        break
    lmt += 1
    print('beginning page %s' % page.name)
    text = page.text()
    wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
    process_start()
    for template in wikitext.filter_templates():
        if template.name.matches('TournamentResultsLine'):
            process_line()
    newtext = str(wikitext)
    if text != newtext:
        print('Saving page %s...' % page.name)
        page.save(newtext, summary=summary)
    else:
        print('Skipping page %s...' % page.name)