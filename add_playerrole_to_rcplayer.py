from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('cod-esports', credentials=credentials)
summary = 'Adding Player role to all Retirement templates'


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template):
        if template.has('player') and template.get('player').value.strip() != '':
            if template.has('status') and template.get('status').value.strip() == '':
                template.remove('status')

            if template.has('role'):
                role = template.get('role').value.strip()
                template.remove('role')
                if role != '':
                    template.add('role', role)
                else:
                    template.add('role', 'Player')
            else:
                template.add('role', 'Player')


TemplateModifier(site, 'Retirement', summary=summary).run()
