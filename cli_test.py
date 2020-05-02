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
                         '--verbose': False,
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

    def test_name(self):
        cli = CLI(self.arguments)
        self.assertEqual(cli.command().name(), 'suggestions')

    def test_execute(self):
        pass

    @patch('client.UserVoiceClient')
    def test_list(self, MockUserVoiceClient):
        self.arguments['list'] = True
        cli = CLI(self.arguments)

        client = MockUserVoiceClient()
        client.suggestions.return_value = [{'id': 1, 'title': 'fake-title1', 'state': 'fake-state1'},
                                           {'id': 2, 'title': 'fake-title2', 'state': 'fake-state2'}]

        rc = cli.command().execute()
        self.assertEqual(rc, 0)

    @patch('client.UserVoiceClient')
    def test_show(self, MockUserVoiceClient):
        self.arguments['show'] = True
        self.arguments['ID'] = 1

        client = MockUserVoiceClient()
        client.suggestion.return_value = {'id': 1, 'title': 'fake-title', 'state': 'fake-state'}

        cli = CLI(self.arguments)

        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_delete(self):
        pass

    def test_create(self):
        pass

if __name__ == '__main__':
    main()