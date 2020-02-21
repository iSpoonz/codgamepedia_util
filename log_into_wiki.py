import mwclient, re


def login(user, wiki):
    with open('password.txt') as f:
        password = f.read().strip()

    with open('password2.txt') as f:
        password2 = f.read().strip()
    if user == 'me':
        site = mwclient.Site('%s.gamepedia.com' % wiki, path='/')
        site.login('Ispoonz@Botspoonz', password)
        return site
    elif user == 'bot':
        site = mwclient.Site('%s.gamepedia.com' % wiki, path='/')
        site.login('Botspoonz@Botspoonz', password2)
        return site

def tl_matches(tl, arr):
	return [_ for _ in arr if tl.name.matches(_)]