from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.gamepedia_client import GamepediaClient
from river_mwclient.errors import EsportsCacheKeyError

credentials = AuthCredentials(user_file='me')

site = EsportsClient('cod', credentials=credentials)

print(site.cache.get('Team', 'tsm', 'link'))

try:
    print(site.cache.get('Team', 'tsm', 'not_a_real_length'))
except EsportsCacheKeyError as e:
    print(e)

site.client.pages['User:Ispoonz/login test'].save('Hello World')