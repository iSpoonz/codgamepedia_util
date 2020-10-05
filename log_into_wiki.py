import mwclient, re


def login(user, wiki):
    with open('username_me.txt') as f:
        username = f.read().strip()

    with open('username_bot.txt') as f:
        username2 = f.read().strip()

    with open('password_me.txt') as f:
        password = f.read().strip()

    with open('password_bot.txt') as f:
        password2 = f.read().strip()
    if user == 'me':
        site = mwclient.Site('%s.gamepedia.com' % wiki, path='/')
        site.login(username, password)
        return site
    elif user == 'bot':
        site = mwclient.Site('%s.gamepedia.com' % wiki, path='/')
        site.login(username2, password2)
        return site

def tl_matches(tl, arr):
	return [_ for _ in arr if tl.name.matches(_)]