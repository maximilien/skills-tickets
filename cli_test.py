# Copyright © 2020 IBM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase
from unittest.mock import patch, Mock

from cli import *

class TestCredentials(TestCase):
    def setUp(self):
        self.hash = {'subdomain': 'fake-domain',
                     'url_callback': 'fake-url-callbnack',
                     'api_key': 'fake-api-key',
                     'api_secret': 'fake-api-secret',
                     'sso_key': 'fake-sso-key',
                     'display_name': 'fake-display-name',
                     'email': 'fake@email.com'}
        self.credentials = Credentials(self.hash)

    def test_subdomain(self):
        self.assertEqual(self.hash['subdomain'], self.credentials.subdomain())

    def test_url_callback(self):
        self.assertEqual(self.hash['url_callback'], self.credentials.url_callback())

    def test_api_key(self):
        self.assertEqual(self.hash['api_key'], self.credentials.api_key())

    def test_api_secret(self):
        self.assertEqual(self.hash['api_secret'], self.credentials.api_secret())

    def test_sso_key(self):
        self.assertEqual(self.hash['sso_key'], self.credentials.sso_key())

    def test_display_name(self):
        self.assertEqual(self.hash['display_name'], self.credentials.display_name())

    def test_email(self):
        self.assertEqual(self.hash['email'], self.credentials.email())

class TestCLI(TestCase):
    def setUp(self):
        self.arguments = {'--api-key': None,
                         '--api-secret': None,
                         '--credentials': './credentials.yml',
                         '--display-name': None,
                         '--email': None,
                         '--help': False,
                         '--sso-key': None,
                         '--subdomain': 'cognitiveclass',
                         '--url-callback': None,
                         '--verbose': False,
                         '--version': False,
                         'BODY': 'body',
                         'ID': None,
                         'TITLE': 'title',
                         'create': True,
                         'list': False,
                         'delete': False,
                         'show': False,
                         'tickets': True}

    def test_command(self):
        self.arguments['tickets'] = True
        cli = CLI(self.arguments)
        self.assertTrue(cli.command() != None)

        self.arguments['suggestions'] = True
        cli = CLI(self.arguments)
        self.assertTrue(cli.command() != None)

    def test_dispatch(self):
        for command_name in ['tickets', 'suggestions']:
            self.arguments[command_name] = True
            for method_name in ['list', 'show', 'delete', 'create']:
                self.arguments[method_name] = True
                cmd = CLI(self.arguments).command()
                self.assertEqual(cmd.name(), command_name)
                self.assertEqual(cmd.dispatch(), getattr(cmd, method_name))
                self.arguments[method_name] = False
            self.arguments[command_name] = False

class TestTickets(TestCase):
    def setUp(self):
        self.arguments = {'--api-key': None,
                         '--api-secret': None,
                         '--credentials': './credentials.yml',
                         '--display-name': None,
                         '--email': None,
                         '--help': False,
                         '--sso-key': None,
                         '--subdomain': 'cognitiveclass',
                         '--url-callback': None,
                         '--show-details': False,
                         '--verbose': False,
                         '--version': False,
                         'BODY': 'body',
                         'ID': None,
                         'TITLE': 'title',
                         'create': True,
                         'list': False,
                         'delete': False,
                         'show': False,
                         'tickets': True}

    def test_name(self):
        cli = CLI(self.arguments)
        self.assertEqual(cli.command().name(), 'tickets')

    def test_execute(self):
        pass

    def test_list(self):
        pass

    def test_show(self):
        pass

    def test_delete(self):
        pass

    def test_create(self):
        pass

class TestSuggestions(TestCase):
    def setUp(self):
        self.arguments = {'--api-key': None,
                         '--api-secret': None,
                         '--credentials': './credentials.yml',
                         '--display-name': None,
                         '--email': None,
                         '--help': False,
                         '--sso-key': None,
                         '--subdomain': 'cognitiveclass',
                         '--url-callback': None,
                         '--show-details': False,
                         '--verbose': False,
                         '--version': False,
                         'BODY': 'body',
                         'ID': None,
                         'TITLE': 'title',
                         'create': True,
                         'list': False,
                         'delete': False,
                         'show': False,
                         'suggestions': True}

    @patch('client.UserVoiceClient')
    def __create_mock_client_get_suggestion(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.get_suggestion.return_value = {'id': 1, 'title': 'fake-title1', 'state': 'fake-state1'}
        return client

    @patch('client.UserVoiceClient')
    def __create_mock_client_get_suggestions(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.get_suggestions.return_value = [{'id': 1, 'title': 'fake-title1', 'state': 'fake-state1'},
                                               {'id': 2, 'title': 'fake-title2', 'state': 'fake-state2'}]
        return client

    def test_name(self):
        cli = CLI(self.arguments)
        self.assertEqual(cli.command().name(), 'suggestions')

    def test_execute(self):
        pass

    def test_list(self):
        self.arguments['list'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_suggestions()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_list_show_details(self):
        self.arguments['list'] = True
        self.arguments['--show-details'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_suggestions()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_show(self):
        self.arguments['show'] = True
        self.arguments['ID'] = 1
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_suggestion()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_create(self):
        pass

    def test_delete(self):
        pass

class TestForums(TestCase):
    def setUp(self):
        self.arguments = {'--api-key': None,
                         '--api-secret': None,
                         '--credentials': './credentials.yml',
                         '--display-name': None,
                         '--email': None,
                         '--help': False,
                         '--sso-key': None,
                         '--subdomain': 'cognitiveclass',
                         '--url-callback': None,
                         '--show-details': False,
                         '--verbose': False,
                         '--version': False,
                         'BODY': 'body',
                         'ID': None,
                         'TITLE': 'title',
                         'create': True,
                         'list': False,
                         'delete': False,
                         'show': False,
                         'forums': True}

    @patch('client.UserVoiceClient')
    def __create_mock_client_get_forum(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.get_forum.return_value = {'id': 1, 'name': 'fake-forum'}
        return client

    @patch('client.UserVoiceClient')
    def __create_mock_client_get_forums(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.get_forums.return_value = [{'id': 1, 'name': 'fake-forum1'},
                                          {'id': 2, 'name': 'fake-forum2'}]
        return client

    def test_name(self):
        cli = CLI(self.arguments)
        self.assertEqual(cli.command().name(), 'forums')

    def test_execute(self):
        pass

    def test_list(self):
        self.arguments['list'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_forums()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_list_show_details(self):
        self.arguments['list'] = True
        self.arguments['--show-details'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_forums()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_show(self):
        self.arguments['show'] = True
        self.arguments['ID'] = 1
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_forum()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

if __name__ == '__main__':
    main()