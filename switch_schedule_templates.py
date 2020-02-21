from log_into_wiki import *
import mwparserfromhell

site = login('me', 'smite-esports')  # Set wiki
summary = 'Fixing Formatting from GS5 to MS'  # Set summary
limit = -1
startat = -1

#################################
# Ignore everything above here
#################################

# pagename = 'Challenger Circuit/2017 Season/Europe/Pre-Summer Relegations'
pointstype = 'bo5'  # bo3, bo3points, bo2, bo3pointsopl

remove_params = ['start', 'end', 'hide', 'nosemantics', 'title', 'streamname']
tb_names = ['tb', 'tiebreakers', 'tiebreaker']

max_scores = {
    'bo3points': 3,
    'bo3pointsopl': 3,
    'none': 1,
    'bo2': 2,
    'bo5': 3
}

# pages_var = [site.pages['Data:' + pagename]]

with open('pages.txt', encoding="utf-8") as f:
    pages = f.readlines()
pages_var = [site.pages[page.strip()] for page in pages]

lmt = 1
for page in pages_var:
    if lmt == limit:
        break
    lmt += 1
    if lmt < startat:
        print("Skipping page %s" % page.name)
    else:
        text = page.text()
        wikitext = mwparserfromhell.parse(text)
        for template in wikitext.filter_templates():
            if template.name.matches('GameSchedule') or template.name.matches('GameSchedule5'):
                template.name = 'MatchSchedule'
                score1 = 0
                score2 = 0
                if template.has('t1score') and template.has('t2score'):
                    if template.get('t1score').value.strip() != '' and template.get('t2score').value.strip() != '':
                        str1 = template.get('t1score').value.strip()
                        str2 = template.get('t2score').value.strip()
                        template.remove('t1score')
                        template.remove('t2score')
                        score1 = 0
                        score2 = 0
                        if str1 == 'FF' or 'W' or 'L':
                            template.add('team1score', str1)
                        if str2 == 'FF' or 'W' or 'L':
                            template.add('team2score', str2)
                        else:
                            score1 = int(str1)
                            score2 = int(str2)
                            template.add('team1score', score1)
                            template.add('team2score', score2)
                        if pointstype == 'bo3points':
                            template.add('team1pointstb', str(score1 - score2), before='date')
                            template.add('team2pointstb', str(score2 - score1), before='date')
                        elif pointstype == 'bo3pointsopl':
                            points1 = score1 + (1 if score2 == 0 else 0)
                            points2 = score2 + (1 if score1 == 0 else 0)
                            template.add('team1points', str(points1), before='date')
                            template.add('team2points', str(points2), before='date')
                        elif pointstype == 'bo2':
                            points1 = 3 if score1 == 2 else score1
                            points2 = 3 if score2 == 2 else score2
                            template.add('team1points', str(points1), before='date')
                            template.add('team2points', str(points2), before='date')
                if template.has('round'):
                    if template.get('round').value.strip().lower() in tb_names:
                        template.add('istb', 'yes', before='round')
                if template.has('post-match'):
                    if template.get('post-match').value.strip() != '':
                        reddit = template.get('post-match').value.strip()
                        template.remove('post-match')
                        template.add('reddit', reddit)
                    else:
                        template.remove('post-match')
                for param in remove_params:
                    if template.has(param):
                        template.remove(param)
                for i in range(0, 5):
                    s = str(i + 1)
                    game = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
                    thisvod = 'vod' + s
                    if template.has(thisvod):
                        game.add('vod', str(template.get(thisvod).value.strip()))
                        template.remove(thisvod)
                    if not template.has('game' + s):
                        template.add('game' + s, str(game))
                if template.has('winner') and template.get('winner').value.strip().lower() == 'draw':
                    template.add('winner', '0')
        newtext = str(wikitext)
        if text != newtext:
            print('Saving page %s...' % page.name)
            page.save(newtext, summary=summary)
        else:
            print('Skipping page %s...' % page.name)
