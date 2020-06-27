from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('cod-esports', credentials=credentials)
summary = 'Renaming parameter: newrole -> new_role'


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template):
        if template.has('newrole'):
            role = template.get('newrole').value.strip()
            template.add('new_role', role, before='newrole')
            template.remove('newrole')


TemplateModifier(site, 'Retirement',
                 summary=summary).run()