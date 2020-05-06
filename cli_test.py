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

import os, tempfile

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
                         'create': False,
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

class CommandTestCase:
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
                         'create': False,
                         'list': False,
                         'delete': False,
                         'show': False}
        self.args = self.arguments

    @patch('client.UserVoiceClient')
    def __create_mock_client(self, MockUserVoiceClient):
        return MockUserVoiceClient()

    def test_verbose(self):
        self.arguments[self.command_name()] = True
        command = CLI(self.arguments).command(self.__create_mock_client())
        if self.arguments['--verbose'] == True:
            self.assertTrue(command.verbose())
        else:
            self.assertFalse(command.verbose())

    def test_name(self):
        cli = CLI(self.arguments)
        self.assertEqual(cli.command().name(), self.command_name())

class TestTickets(CommandTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.arguments['tickets'] = True

    def command_name(self):
        return "tickets"

    @patch('client.UserVoiceClient')
    def __create_mock_client_get_ticket(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.get_ticket.return_value = {'id': 1, 'ticket_id': 1, 'title': 'fake-title1'}
        return client

    @patch('client.UserVoiceClient')
    def __create_mock_client_get_tickets(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.get_tickets.return_value = [{'id': 1, 'ticket_id': 1, 'title': 'fake-title1'},
                                           {'id': 2, 'ticket_id': 1, 'title': 'fake-title2'}]
        return client

    @patch('client.UserVoiceClient')
    def __create_mock_client_post_ticket(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.post_ticket.return_value = {'id': 1, 'ticket_id': 1, 'title': 'fake-title1'}
        return client

    @patch('client.UserVoiceClient')
    def __create_mock_client_put_delete_ticket(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.put_delete_ticket.return_value = 200
        return client

    def test_execute(self):
        self.arguments['fake'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_tickets()
        with self.assertRaises(Exception) as context:
            cli.command(client).execute()

    def test_list(self):
        self.arguments['list'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_tickets()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_list_show_details(self):
        self.arguments['list'] = True
        self.arguments['--show-details'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_ticket()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_show(self):
        self.arguments['show'] = True
        self.arguments['ID'] = 1
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_ticket()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_create(self):
        self.arguments['create'] = True
        self.arguments['TITLE'] = "fake-title"
        self.arguments['BODY'] = "fake-body"
        cli = CLI(self.arguments)
        client = self.__create_mock_client_post_ticket()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_delete(self):
        self.arguments['delete'] = True
        self.arguments['ID'] = 1
        cli = CLI(self.arguments)
        client = self.__create_mock_client_put_delete_ticket()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

class TestSuggestions(CommandTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.arguments['suggestions'] = True

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

    @patch('client.UserVoiceClient')
    def __create_mock_client_post_suggestion(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.post_suggestion.return_value = {'id': 1, 'title': 'fake-title1', 'state': 'fake-state1'}
        return client

    @patch('client.UserVoiceClient')
    def __create_mock_client_put_delete_suggestion(self, MockUserVoiceClient):
        client = MockUserVoiceClient()
        client.put_delete_suggestion.return_value = 200
        return client

    def command_name(self):
        return "suggestions"

    def test_execute(self):
        self.arguments['fake'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_suggestions()
        with self.assertRaises(Exception) as context:
            cli.command(client).execute()

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
        self.arguments['create'] = True
        self.arguments['FORUM_ID'] = 1
        self.arguments['TITLE'] = "fake-title"
        self.arguments['BODY'] = "fake-body"
        cli = CLI(self.arguments)
        client = self.__create_mock_client_post_suggestion()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

    def test_delete(self):
        self.arguments['delete'] = True
        self.arguments['ID'] = 1
        cli = CLI(self.arguments)
        client = self.__create_mock_client_put_delete_suggestion()
        rc = cli.command(client).execute()
        self.assertEqual(rc, 0)

class TestForums(CommandTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.arguments['forums'] = True

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

    def command_name(self):
        return "forums"

    def test_execute(self):
        self.arguments['fake'] = True
        cli = CLI(self.arguments)
        client = self.__create_mock_client_get_forums()
        with self.assertRaises(Exception) as context:
            cli.command(client).execute()

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

class TestCSV(CommandTestCase):
    def setUp(self):
        super().setUp()
        self.arguments = {**self.arguments, **{'FILE': None,
                                               'CLUSTER': None,
                                               'split': False,
                                               'verify': False,
                                               'csv': True}}
        TEST_CSV = """, id, Ticket Number, name, cluster
        1, 11, 12, fake-name1, fake cluster1
        2, 21, 22, fake-name1, fake cluster2
        3, 31, 32, fake-name1, fake cluster1
        """
        file, self.input_filepath = tempfile.mkstemp()
        with os.fdopen(file, 'w') as tmp:
            tmp.write(TEST_CSV)

    def tearDown(self):
        os.remove(self.input_filepath)

    def command_name(self):
        return "csv"

    def test_execute(self):
        self.arguments['fake'] = True
        cli = CLI(self.arguments)
        with self.assertRaises(Exception) as context:
            cli.command(client).execute()

    def test_verify(self):
        self.arguments['FILE'] = self.input_filepath
        self.arguments['verify'] = True
        command = CLI(self.arguments).command()
        rc = command.execute()
        self.assertEqual(rc, 0)
        self.assertEqual(len(command.entries(), 3))
        self.assertEqual(len(command.clusters(), 2))
        self.assertEqual(len(command.keys(), 5))
        self.assertEqual(command.keys(), ['', 'id', 'ticket_number', 'name', 'cluster'])

    def test_split(self):
        self.arguments['FILE'] = self.input_filepath
        self.arguments['CLUSTER'] = 'fake cluster1'
        self.arguments['split'] = True
        command = CLI(self.arguments).command()
        rc = command.execute()
        self.assertEqual(rc, 0)

if __name__ == '__main__':
    main()