from log_into_wiki import *
import mwparserfromhell, re, html

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Converting old tournament results templates to new'  # Set summary

limit = -1

pages = site.pages['Template:TournamentResultsStart'].embeddedin(namespace=0)

# https://regex101.com/r/HN75H4/3/
regex = r"===(.+?)===\n(.+?) (?:.+?)\n"
regexref = r"===(.+?)===\n(.+?) (?:.+?)<ref>(.+?)</ref>\n"
myr = r"===(?: |)\n(.+?)\n{{TournamentResultsStart"
blank_lines = r"^\s+$"

lmt = 0


# pages = [site.pages['RUSH Infinite Warfare 2017']]


def process_start():
    match = re.search(myr, str(wikitext))
    # print(match)
    if match:
        """"
        totalprize = match[1]
        prizeunit = "ZAR"
        #if match[3] is not None and match[3] != '':
        #    ref = match[3]
        """
        linelist = process_line()

        for template in wikitext.filter_templates():
            if template.name.matches('TournamentResultsStart'):
                template.name = 'TournamentResults'
                if template.has('pointstitle'):
                    template.add('points', 'yes\n')
                checker = None
                if template.has('noprize'):
                    checker = True
                    template.remove('noprize')
                if template.has('noteams'):
                    template.remove('noteams')
                """
            #    if match[3] is not None and match[3] != '':
            #        template.add('prize_ref', ref + '\n')
                if totalprize != '' and prizeunit != '':
                    template.add('prize', 'yes')
                    template.add('prizeunit', prizeunit)
                    template.add('totalprize', totalprize + linelist)
                else:
                    template.add('noprize', 'yes' + linelist)
                """
                if checker:
                    template.add('noprize', 'yes' + linelist)
                else:
                    template.add('prize', 'yes' + linelist)

            if template.name.matches('TournamentResultsEnd'):
                wikitext.remove(template)
            if template.name.matches('TournamentResults/Line'):
                wikitext.remove(template)
    return None


def process_line():
    linelist = ''
    points = 'x'
    place = 'x'
    prev_points = 'y'
    prev_place = 'y'
    for template2 in wikitext.filter_templates():
        if template2.name.matches('TournamentResultsLine'):
            template2.name = 'TournamentResults/Line'
            if template2.has('prizeunit'):
                template2.remove('prizeunit')
            if template2.has('points') and template2.get('points').value.strip() != '':
                if template2.has('sameplaces'):
                    points = template2.get('points').value.strip()
                    place = template2.get('place').value.strip()
                if prev_place == place and prev_points == points:
                    template2.remove('points')
                    template2.add('points', prev_points, before='team')
            i = 1
            playerDict = {}
            roleDict = {}
            # print(i)
            while template2.has('p' + str(i)):
                if template2.has('p' + str(i) + 'link'):
                    playerDict["player{0}".format(i)] = template2.get('p' + str(i) + 'link').value.strip()
                    template2.remove('p' + str(i))
                    template2.remove('p' + str(i) + 'link')
                else:
                    playerDict["player{0}".format(i)] = template2.get('p' + str(i)).value.strip()
                    template2.remove('p' + str(i))
                if template2.has('p' + str(i) + 'role'):
                    roleDict["role{0}".format(i)] = template2.get('p' + str(i) + 'role').value.strip()
                    template2.remove('p' + str(i) + 'role')
                else:
                    roleDict["role{0}".format(i)] = ''
                i += 1
            # print(playerDict)
            # print(roleDict)

            playerlist = ''
            for x in range(1, len(playerDict) + 1):
                t = mwparserfromhell.nodes.template.Template('TeamRoster/Line')
                t.add('player', playerDict["player{0}".format(x)])
                if roleDict["role{0}".format(x)] != '':
                    t.add('role', roleDict["role{0}".format(x)])
                playerlist += str(t)

            template2.add('roster', playerlist)
            # print(playerlist)
            line = "\n|" + str(template2)
            linelist += str(line)

            if template2.has('sameplaces'):
                prev_points = points
                prev_place = place
                template2.remove('sameplaces')
    # print(html.unescape(linelist))
    return linelist


for page in pages:
    if lmt == limit:
        break
    lmt += 1
    print('beginning page %s' % page.name)
    text = page.text()
    wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
    process_start()
    wikitext = re.sub(myr, '===\n', str(wikitext))
    wikitext = re.sub(blank_lines, '', str(wikitext), flags=re.MULTILINE)
    newtext = str(wikitext)
    if text != newtext:
        print('Saving page %s...' % page.name)
        page.save(html.unescape(newtext), summary=summary)
    else:
        print('Skipping page %s...' % page.name)
