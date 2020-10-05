from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('cod-esports', credentials=credentials)  # Set wiki
summary = 'Use just |player=, no |link='  # Set summary


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template):
        if not template.has('link'):
            return
        player = template.get('player').value.strip()
        link = template.get('link').value.strip()
        if not link.lower().startswith(player.lower()):
            return
        template.remove('link')
        template.add('player', link, before='flag')


TemplateModifier(site, 'TeamRoster/Line',
                 summary=summary).run()