from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('fortnite-esports', credentials=credentials)
summary = 'Creating player tooltips'

pages_to_make = [
    {
        'match': 'Infobox Player',
        'pages': [
            {
                'pattern': 'Tooltip:{}',
                'text': '{{PlayerTooltip}}',
            },
        ]
    },
]

startat_page = 'Fluva'
passed_startat = False
limit = -1
lmt = 0

for i, page in enumerate(site.pages_using('Infobox Player')):
    if lmt == limit:
        break
    if page.name == startat_page:
        passed_startat = True
    if not passed_startat:
        continue
    if page.namespace == 2:
        continue
    lmt += 1
    text = page.text()
    this_pages = None
    for page_set in pages_to_make:
        if page_set['match'] in text:
            this_pages = page_set['pages']
            break
    if this_pages is None:
        continue
    for item in this_pages:
        subpage = item['pattern'].format(page.name)
        if site.client.pages[subpage].exists:
            print('skipping page: ' + page.name)
            continue
        print('Saving page %s...' % page.name)
        site.client.pages[subpage].save(item['text'], summary=summary)
