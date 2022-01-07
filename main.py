import json
from types import SimpleNamespace
from typing import List

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import BooleanProperty

import taas

settings_panel = """
[
    { "type": "title",
      "title": "Login" },

    { "type": "string",
      "title": "Username",
      "section": "login",
      "key": "username"},

    { "type": "string",
      "title": "Password",
      "section": "login",
      "key": "password"}
]
"""


class TaaSGUIApp(App):
    disable_buttons = BooleanProperty(taas.auth_token is None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def on_start(self):
        # data = '[{"id": "1", "name": "jack", "description": "", "revision": 0, "templateVersion": "", "tags": [""]}]'
        # j: List[taas.TestCampaign] = json.loads(
        #     data, object_hook=lambda d: taas.TestCampaign(**d))

    def build_config(self, config):
        config.setdefaults('login', {
            'Username': '',
            'Password': '',
        })

    def build_settings(self, settings):
        settings.add_json_panel(
            'App Settings', self.config, data=settings_panel)

    def log(self, text, append=False):
        """Write something to the log box"""
        if append:
            text = f'{self.root.ids.log.text}\n{str(text)}'
        self.root.ids.log.text = str(text)

    def on_auth(self):
        self.log('Getting auth token...')
        username = self.config.get('login', 'username')
        password = self.config.get('login', 'password')
        if not username or not password:
            self.log('Enter username and password in the settings', append=True)
            return
        r = taas.get_auth_token(username, password)
        self.disable_buttons = False
        self.log(r, append=True)

    def on_get_campaigns(self, name):
        self.log('Getting test campaigns...')
        success, r = taas.get_test_campaigns(name)
        self.log(r, append=True)
        if success:
            # Parse the json result as a list of campaigns
            campaigns: List[taas.TestCampaign] = json.loads(
                r, object_hook=lambda d: taas.TestCampaign(**d))
            taas.campaigns.clear()
            for campaign in campaigns:
                taas.campaigns[campaign.name] = campaign
            self.root.ids.campaign_spinner.values = taas.campaigns.keys()

    def on_excute(self, campaign_name):
        self.log('Executing test campaign...')
        r = taas.execute_test_campaign(campaign_name)
        self.log(r, append=True)

    def on_stop(self):
        self.log('Stopping test campaign...')
        r = taas.stop_running_test_campaign()
        self.log(r, append=True)

    def on_status(self):
        self.log('Getting test status...')
        r = taas.get_test_campaign_status()
        self.log(r, append=True)


def main():
    Window.top, Window.left = (100, 100)
    Window.clearcolor = (0.5, 0.5, 0.5, 1)
    TaaSGUIApp().run()


if __name__ == '__main__':
    main()
    # x = AsyncImage(source='https://i.stack.imgur.com/gN9W5.png')
