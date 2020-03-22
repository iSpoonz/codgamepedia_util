from log_into_wiki import *
import mwparserfromhell, re

site = login('bot', 'cod-esports')  # Set wiki
summary = 'Attempting to parse timeline content as templates'  # Set summary

page_type = 'teams'  # tournament, players, teams

limit = 1
startat_page = None
print(startat_page)
# startat_page = 'User:Ispoonz/TimelineRegexTest'
template_by_type = {
    'players': 'Player',
    'teams': 'Team',
    'tournament': 'Tournament'
}
this_template = site.pages['Template:Infobox ' + template_by_type[page_type]]  # Set template
pages = this_template.embeddedin()

months = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?"
date = r" *(\d+)(?:st|th|rd|nd)?[.,]? ?(?:\d\d\d\d,? ?)?(?: *\- *)?"
nodatesentence = r" \(approx(.+?),(.+?) (rejoins|rejoin|leaves|leave|joins|join|retires)(.+?)((.+?) (rejoins|rejoin|leaves|leave|joins|join)(.+?)|(.*))"
sentence = r"(.+?) (rejoins|rejoin|leaves|leave|joins|join|retires|becomes)(.+?)((.+?) (rejoins|rejoin|leaves|leave|joins|join)(.+?)|)(?:| )"
reference = r"(?:| )\[(.+?) ([^\]]*)\] ?(?:\([\dms]+\) )? ?(?: *\- *)?''(.+?)''(?:| )"
alt1 = r"(<ref>\[(.+?) ([^\]]*)\] ?(?:\([\dms]+\) )? ?(?: *\- *)?''(.+?)''</ref>|(.+?) (rejoins|rejoin|leaves|leave|joins|join)(.+?)((.+?) (rejoins|rejoin|leaves|leave|joins|join)(.+?)|)<ref>\[(.+?) ([^\]]*)\] ?(?:\([\dms]+\) )? ?(?: *\- *)?''(.+?)''</ref>|)"
alt2 = r"(<ref>\[(.+?) ([^\]]*)\] ?(?:\([\dms]+\) )? ?(?: *\- *)?''(.+?)''</ref>|)"

identify_players = r"({{bl\||{{Bl\||\[\[|''')(.+?)(\||}}|]]|''')"
strip_role = r"^\s(?:(?:as|) (?:a|an|the|)(.+?)|(.+?))\."

regex = r"^\* ?" + months + date + sentence + '<ref>' + reference + '</ref>' + alt1 + alt2
noref = r"^\* ?" + months + date + sentence
approxdate = r"^\* ?" + months + nodatesentence

passed_startat = False if startat_page else True
lmt = 0

pages = [site.pages["Evil Geniuses"]]
team_region = 'NA'  # CDL, NA, EU etc


def process_line(line):
    match = re.match(regex, line)
    # print(match[4])

    if match:
        string1 = match[3]
        step1 = re.finditer(identify_players, str(string1))  # find player names inside brackets
        step2 = ''
        if match[7] != '':
            string2 = match[7]
            step2 = re.finditer(identify_players, str(string2))  # find player names inside brackets

        string1role = ''
        if match[5] != '.' and match[5] is not None:
            role1regex = re.match(strip_role, match[5])  # remove as, and etc from end of sentence 1 to identify role
            string1role = role1regex[1] or role1regex[2]

        string2role = ''
        if match[9] != '.' and match[9] is not None:
            role2regex = re.match(strip_role, match[9])
            string2role = role2regex[1] or role2regex[2]

        # up to 3 references can be added to the sourcelist
        sourcelist = ''
        s = mwparserfromhell.nodes.template.Template('Source')
        s.add('link', match[10])
        s.add('title', match[11])
        s.add('desc', match[12])
        sourcelist += str(s)
        if match[14] is not None and match[14].strip() != '':
            s2 = mwparserfromhell.nodes.template.Template('Source')
            s2.add('link', match[14])
            s2.add('title', match[15])
            s2.add('desc', match[16])
            sourcelist += str(s2)
        if match[28] is not None and match[28].strip() != '':
            s3 = mwparserfromhell.nodes.template.Template('Source')
            s3.add('link', match[28])
            s3.add('title', match[29])
            s3.add('desc', match[30])
            sourcelist += str(s3)
        print(sourcelist)

        listofrcplayer = ''
        rfa = ''
        for player in step1:  # loop through step1 list making new template for each new player
            r = mwparserfromhell.nodes.template.Template('RCPlayer')
            rfa = player.group(2)
            r.add('player', player.group(2))
            if string1role in ['substitute', 'Substitute', 'substitutes']:
                r.add('sub', 'yes')
            elif string1role in ['restricted free agent', 'Restricted Free Agent']:
                r.add('status', 'opportunities')
            elif string1role in ['inactive']:
                r.add('status', 'inactive')
            elif string1role != '':
                r.add('role', string1role)
            if match[4] in ['rejoin', 'rejoins']:
                r.add('rejoin', 'yes')
            listofrcplayer += str(r)
        rfapre = mwparserfromhell.nodes.template.Template('RCPlayer')
        rfapre.add('player', rfa)
        print(listofrcplayer)

        listofrcplayer2 = ''
        for player2 in step2:
            p = mwparserfromhell.nodes.template.Template('RCPlayer')
            p.add('player', player2.group(2))
            if string2role in ['substitute', 'Substitute', 'substitutes']:
                p.add('sub', 'yes')
            else:
                p.add('role', string2role)
            if match[8] in ['rejoin', 'rejoins']:
                p.add('rejoin', 'yes')
            listofrcplayer2 += str(p)
        print(listofrcplayer2)

        if match[4] == 'retires':
            r = mwparserfromhell.nodes.template.Template('Retirement')
            r.add('player', player.group(2))
            r.add('region', team_region)
            r.add('team', page.name)
            r.add('source', sourcelist)
            r.add('date', match[1] + ' ' + match[2])
            lines[j] = str(r)
            return r
        else:
            t = mwparserfromhell.nodes.template.Template('RosterChangeData/Line')
            t.add('team', page.name)
            t.add('region', team_region)
            t.add('source', sourcelist)
            if match[4] in ['join', 'joins'] and match[8] in ['leave', 'leaves']:
                t.add('pre', listofrcplayer2)
                t.add('post', listofrcplayer)
            elif match[8] in ['leave', 'leaves']:
                t.add('pre', listofrcplayer2)

            if match[8] in ['join', 'joins'] and match[4] in ['leave', 'leaves']:
                t.add('pre', listofrcplayer)
                t.add('post', listofrcplayer2)
            elif match[4] in ['leave', 'leaves']:
                t.add('pre', listofrcplayer)
            elif match[4] in ['join', 'joins']:
                t.add('post', listofrcplayer)

            if match[4] in ['join', 'joins'] and match[8] in ['join', 'joins']:
                t.add('post', listofrcplayer + listofrcplayer2)

            if match[4] in ['rejoins', 'rejoin'] and match[8] in ['join', 'joins']:
                t.add('post', listofrcplayer + listofrcplayer2)
            elif match[4] in ['rejoins', 'rejoin'] and match[8] in ['leave', 'leaves']:
                t.add('pre', listofrcplayer2)
                t.add('post', listofrcplayer)
            elif match[8] in ['rejoins', 'rejoin'] and match[4] in ['join', 'joins']:
                t.add('post', listofrcplayer + listofrcplayer2)
            elif match[8] in ['rejoins', 'rejoin'] and match[4] in ['leave', 'leaves']:
                t.add('pre', listofrcplayer)
                t.add('post', listofrcplayer2)
            elif match[4] in ['rejoins', 'rejoin']:
                t.add('post', listofrcplayer)

            if string1role in ['restricted free agent', 'Restricted Free Agent']:
                t.add('pre', rfapre)
                t.add('post', listofrcplayer)

            if string1role in ['inactive']:
                t.add('pre', rfapre)
                t.add('post', listofrcplayer)
            t.add('date', match[1] + ' ' + match[2])
            lines[j] = str(t)
            return t

    match = re.match(noref, line)
    if match:
        string1 = match[3]
        step1 = re.finditer(identify_players, str(string1))  # find player names inside brackets

        step2 = ''
        if match[7] != '':
            string2 = match[7]
            step2 = re.finditer(identify_players, str(string2))  # find player names inside brackets

        string1role = ''
        if match[5] != '.' and match[5] is not None:
            role1regex = re.match(strip_role, match[5])  # remove as, and etc from end of sentence 1 to identify role
            string1role = role1regex[1] or role1regex[2]

        string2role = ''
        if match[9] != '.' and match[9] is not None:
            role2regex = re.match(strip_role, match[9])
            string2role = role2regex[1] or role2regex[2]

        listofrcplayer = ''
        for player in step1:  # loop through step1 list making new template for each new player
            r = mwparserfromhell.nodes.template.Template('RCPlayer')
            r.add('player', player.group(2))
            if string1role in ['substitute', 'Substitute', 'substitutes']:
                r.add('sub', 'yes')
            else:
                r.add('role', string1role)
            if match[4] in ['rejoin', 'rejoins']:
                r.add('rejoin', 'yes')
            listofrcplayer += str(r)
        print(listofrcplayer)

        listofrcplayer2 = ''
        for player2 in step2:
            p = mwparserfromhell.nodes.template.Template('RCPlayer')
            p.add('player', player2.group(2))
            if string2role in ['substitute', 'Substitute', 'substitutes']:
                p.add('sub', 'yes')
            else:
                p.add('role', string2role)
            if match[8] in ['rejoin', 'rejoins']:
                p.add('rejoin', 'yes')
            listofrcplayer2 += str(p)
        print(listofrcplayer2)

        t = mwparserfromhell.nodes.template.Template('RosterChangeData/Line')
        t.add('team', page.name)
        t.add('region', team_region)  # DONT KNOW HOW TO GET REGION
        if match[4] in ['join', 'joins'] and match[8] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer2)
            t.add('post', listofrcplayer)
        elif match[8] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer2)

        if match[8] in ['join', 'joins'] and match[4] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer)
            t.add('post', listofrcplayer2)
        elif match[4] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer)
        elif match[4] in ['join', 'joins']:
            t.add('post', listofrcplayer)

        if match[4] in ['rejoins', 'rejoin'] and match[8] in ['join', 'joins']:
            t.add('post', listofrcplayer + listofrcplayer2)
        elif match[4] in ['rejoins', 'rejoin'] and match[8] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer2)
            t.add('post', listofrcplayer)
        elif match[8] in ['rejoins', 'rejoin'] and match[4] in ['join', 'joins']:
            t.add('post', listofrcplayer + listofrcplayer2)
        elif match[8] in ['rejoins', 'rejoin'] and match[4] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer)
            t.add('post', listofrcplayer2)
        elif match[4] in ['rejoins', 'rejoin']:
            t.add('post', listofrcplayer)
        t.add('date', match[1] + ' ' + match[2])
        lines[j] = str(t)
        return t

    match = re.match(approxdate, line)
    if match:
        string1 = match[3]
        step1 = re.finditer(identify_players, str(string1))  # find player names inside brackets

        step2 = ''
        if match[7] != '':
            string2 = match[7]
            step2 = re.finditer(identify_players, str(string2))  # find player names inside brackets

        string1role = ''
        if match[10] != '' and match[10] is not None:
            role1regex = re.match(strip_role, ' ' + str(match[10]))  # remove as, and etc from end of sentence 1 to identify role
            string1role = role1regex[1] or role1regex[2]

        listofrcplayer = ''
        for player in step1:  # loop through step1 list making new template for each new player
            r = mwparserfromhell.nodes.template.Template('RCPlayer')
            r.add('player', player.group(2))
            if string1role in ['substitute', 'Substitute', 'substitutes']:
                r.add('sub', 'yes')
            else:
                r.add('role', string1role)
            if match[4] in ['rejoin', 'rejoins']:
                r.add('rejoin', 'yes')
            listofrcplayer += str(r)
        print(listofrcplayer)

        listofrcplayer2 = ''
        for player2 in step2:
            p = mwparserfromhell.nodes.template.Template('RCPlayer')
            p.add('player', player2.group(2))
            if match[8] in ['rejoin', 'rejoins']:
                r.add('rejoin', 'yes')
            listofrcplayer2 += str(p)
        print(listofrcplayer2)

        t = mwparserfromhell.nodes.template.Template('RosterChangeData/Line')
        t.add('team', page.name)
        t.add('region', team_region)  # DONT KNOW HOW TO GET REGION
        t.add('display_date', '')
        t.add('approx', 'yes')
        if match[4] in ['join', 'joins'] and match[8] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer2)
            t.add('post', listofrcplayer)
        elif match[8] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer2)

        if match[8] in ['join', 'joins'] and match[4] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer)
            t.add('post', listofrcplayer2)
        elif match[4] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer)
        elif match[4] in ['join', 'joins']:
            t.add('post', listofrcplayer)

        if match[4] in ['rejoins', 'rejoin'] and match[8] in ['join', 'joins']:
            t.add('post', listofrcplayer + listofrcplayer2)
        elif match[4] in ['rejoins', 'rejoin'] and match[8] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer2)
            t.add('post', listofrcplayer)
        elif match[8] in ['rejoins', 'rejoin'] and match[4] in ['join', 'joins']:
            t.add('post', listofrcplayer + listofrcplayer2)
        elif match[8] in ['rejoins', 'rejoin'] and match[4] in ['leave', 'leaves']:
            t.add('pre', listofrcplayer)
            t.add('post', listofrcplayer2)
        elif match[4] in ['rejoins', 'rejoin']:
            t.add('post', listofrcplayer)
        t.add('date', match[1] + ' 01')
        lines[j] = str(t)
        return t
    return None


for page in pages:
    if lmt == limit:
        break
    if startat_page and page.name == startat_page:
        passed_startat = True
    if not passed_startat:  # or ('2019' not in page.name and '2018' not in page.name):
        print("Skipping page %s" % page.name)
        continue
    lmt += 1
    this_page = page
    print('beginning page %s' % page.name)
    text = this_page.text()
    wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
    is_right_type = False
    for template in wikitext.filter_templates(recursive=False):
        if template.name.matches('Infobox ' + template_by_type[page_type]):
            is_right_type = True
        if tl_matches(template, ['TD', 'TDRight', 'TabsDynamic', 'TDR']) and is_right_type:
            i = 1
            while template.has('content' + str(i)):
                content = template.get('content' + str(i)).value.strip()
                lines = content.split('\n')
                for j, line in enumerate(lines):
                    try:
                        tl = process_line(line)
                    except TypeError:
                        print(TypeError)
                        pass
                    if tl:
                        lines[j] = str(tl)
                template.add('content' + str(i), '\n'.join(lines))
                i += 1

    newtext = str(wikitext)
    if text != newtext:
        print('Saving page %s...' % this_page.name)
        this_page.save(newtext, summary=summary)
    else:
        pass
    # print('Skipping page %s...' % this_page.name)