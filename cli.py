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

import yaml, csv, os.path

from client import UserVoiceClient

VERBOSE=False

class Console:
    def print(msg):
        if VERBOSE:
            print(msg)

class Credentials:
    def __init__(self, hash):
        self.hash = hash

    def subdomain(self):
        return self.hash['subdomain']

    def url_callback(self):
        return self.hash['url_callback']

    def api_key(self):
        return self.hash['api_key']

    def api_secret(self):
        return self.hash['api_secret']

    def sso_key(self):
        return self.hash['sso_key']

    def display_name(self):
        return self.hash['display_name']

    def email(self):
        return self.hash['email']

class CLI:
    def __init__(self, args):
        self.args = args
        self.credentials = self.__setup_credentials()
        if self.args['--verbose']:
            VERBOSE = True

    def __parse_credentials(self):
        credentials_hash = {'subdomain': '',
            'url_callback': '',
            'api_key': '',
            'api_secret': '',
            'sso_key': '',
            'display_name': '',
            'email': ''}
        file_name = self.args['--credentials']
        if file_name:
            try:
                with open(file_name) as file:
                    loaded_credentials = yaml.load(file, Loader=yaml.FullLoader)
                    credentials_hash.update(loaded_credentials)

            except:
                Console.print("Error opening credentials file: {file_name}".format(file_name=file_name))
        return credentials_hash

    def __setup_credentials(self):
        credentials_hash = self.__parse_credentials()
        # Server
        if self.args['--subdomain'] and self.args['--credentials']:
            Console.print("WARNING: using --subdomain value in credentials")
            credentials_hash['subdomain'] = self.args['--subdomain']
        else:
            self.args['--subdomain'] = credentials_hash['subdomain']

        if self.args['--url-callback'] and self.args['--credentials']:
            Console.print("WARNING: using --url-callback value in credentials")
            credentials_hash['url_callback'] = self.args['--url-callback']
        else:
            self.args['--url-callback'] = credentials_hash['url_callback']

        # APIs
        if self.args['--api-key'] and self.args['--credentials']:
            Console.print("WARNING: using --api-key value in credentials")
            credentials_hash['api_key'] = self.args['--api-key']
        else:
            self.args['--api-key'] = credentials_hash['api_key']

        if self.args['--api-secret'] and self.args['--credentials']:
            Console.print("WARNING: using --api-secret value in credentials")
            credentials_hash['api_secret'] = self.args['--api-secret']
        else:
            self.args['--api-secret'] = credentials_hash['api_secret']

        if self.args['--sso-key'] and self.args['--credentials']:
            Console.print("WARNING: using --sso-key value in credentials")
            credentials_hash['sso_key'] = self.args['--sso-key']
        else:
            self.args['--sso-key'] = credentials_hash['sso_key']

        # User
        if self.args['--display-name'] and self.args['--credentials']:
            Console.print("WARNING: using --display-name value in credentials")
            credentials_hash['display_name'] = self.args['--display-name']
        else:
            self.args['--display-name'] = credentials_hash['display_name']

        if self.args['--email'] and self.args['--credentials']:
            Console.print("WARNING: using --email value in credentials")
            credentials_hash['email'] = self.args['--email']
        else:
            self.args['--email'] = credentials_hash['email']
        return Credentials(credentials_hash)

    def command(self, client=None):
        if client == None:
            client = UserVoiceClient(self.credentials)

        if self.args.get('tickets') and self.args['tickets']:
            return Tickets(self.args, self.credentials, client)
        elif self.args.get('suggestions') and self.args['suggestions']:
            return Suggestions(self.args, self.credentials, client)
        elif self.args.get('forums') and self.args['forums']:
            return Forums(self.args, self.credentials, client)
        elif self.args.get('csv') and self.args['csv']:
            return CSV(self.args, self.credentials, client)
        else:
            raise Exception("Invalid command")

class Command:
    def __init__(self, args, credentials, client):
        self.args = args
        self.credentials = credentials
        self.client = client

    def verbose(self):
        return self.args['--verbose']

    def execute(self):
        func = self.dispatch()
        rc = func()
        if rc == None:
            return 0
        else:
            if isinstance(rc, int):
                return rc
            else:
                return -1

    def dispatch(self):
        if self.args['list']:
            return self.list
        elif self.args['show']:
            return self.show
        elif self.args['delete']:
            return self.delete
        elif self.args['create']:
            return self.create
        elif self.args['verify']:
            return self.verify
        elif self.args['split']:
            return self.split
        else:
            raise Exception("Invalid subcommand")

# tickets command group
class Tickets(Command):
    def __init__(self, args, credentials, client):
        self.args = args
        super().__init__(self.args, credentials, client)

    def __print(self, ticket):
        print("Ticket: {id} ticket_id: {ticket_id}, title: '{title}'".format(**ticket))
        if self.args['--show-details']:
            print("------")

    def name(self):
      return "tickets"

    def list(self):
        tickets = self.client.get_tickets()
        print("Found '{len}' tickets".format(len=len(tickets)))
        if self.args['--show-details']:
            i = 1
            for ticket in tickets:
                print("{no}. ID: '{id}', ticket_id: {ticket_id}, title: '{title}'".format(no=i, id=ticket['id'], title=ticket['title']))
                i += 1
        return 0

    def show(self):
        ticket = self.client.get_ticket(self.args['ID'])
        print("Ticket: {id} ticket_id: {ticket_id} title: '{title}'".format(**ticket))
        self.__print(ticket)
        return 0

    def create(self):
        ticket = self.client.post_ticket(self.args['TITLE'], self.args['BODY'])
        self.__print(ticket)
        return 0

    def delete(self):
        rc = self.client.put_delete_ticket(self.args['ID'])
        if rc == 200:
            print("Ticket '{id}' deleted".format(id=self.args['ID']))
        else:
            print("🔥 deleting ticket '{id}' API return code: {rc}".format(id=self.args['ID'], rc=rc))
            return rc
        return 0

# suggestions command group
class Suggestions(Command):
    def __init__(self, args, credentials, client):
        self.args = args
        super().__init__(self.args, credentials, client)

    def __print(self, suggestion):
        print("Suggestion: {id} title: '{title}' is currently '{state}'".format(**suggestion))
        if self.args['--show-details']:
            print("  referrer: {referrer}".format(referrer=suggestion['referrer']))
            print("  vote_count: {vote_count}, subscriber_count: {subscriber_count}, comments_count: {comments_count}, supporters_count: {supporters_count}".format(vote_count=suggestion['vote_count'], subscriber_count=suggestion['subscriber_count'], comments_count=suggestion['comments_count'], supporters_count=suggestion['supporters_count']))
            print("  category: {category}, status: {status}, response: {response}".format(category=suggestion['category']['name'], status=suggestion['status'], response=suggestion['response']))
            print("  text: {text}".format(text=suggestion['text']))
            print("------")

    def name(self):
        return "suggestions"

    def list(self):
        suggestions = self.client.get_suggestions()
        print("Found '{len}' suggestions".format(len=len(suggestions)))
        if self.args['--show-details']:
            i = 1
            for suggestion in suggestions:
                print("{no}. ID: '{id}', title: '{title}', state: '{state}'".format(no=i, id=suggestion['id'], title=suggestion['title'], state=suggestion['state']))
                i += 1
        return 0

    def show(self):
        suggestion = self.client.get_suggestion(self.args['ID'])
        self.__print(suggestion)
        return 0

    def create(self):
        suggestion = self.client.post_suggestion(self.args['FORUM_ID'], self.args['TITLE'], self.args['BODY'])
        self.__print(suggestion)
        return 0

    def delete(self):
        rc = self.client.put_delete_suggestion(self.args['ID'])
        if rc == 200:
            print("Suggestion '{id}' deleted".format(id=self.args['ID']))
        else:
            print("🔥 deleting suggestion '{id}' API return code: {rc}".format(id=self.args['ID'], rc=rc))
            return rc
        return 0

# forums command group
class Forums(Command):
    def __init__(self, args, credentials, client):
        self.args = args
        super().__init__(self.args, credentials, client)

    def name(self):
      return "forums"

    def list(self):
        forums = self.client.get_forums()
        print("Found '{len}' forums".format(len=len(forums)))
        if self.args['--show-details']:
            i = 1
            for forum in forums:
                print("{no}. ID: '{id}', name: '{name}'".format(no=i, id=forum['id'], name=forum['name']))
                i += 1
        return 0

    def show(self):
        forum = self.client.get_forum(self.args['ID'])
        print("Forum: '{id}', name: '{name}'".format(id=forum['id'], name=forum['name']))
        return 0

# csv command group
class CSV(Command):
    def __init__(self, args, credentials, client):
        self.args = args
        super().__init__(self.args, credentials, client)
        self.keys = []
        self.entries = []
        self.clusters = []

    def __check_file(self, filename):
        if os.path.isfile(filename):
            return True
        else:
            print("🔥 CSV file '{filename}' does not exist".format(filename=filename))
            return False

    def __normalize_keys(self, keys):
        nkeys = []
        for key in keys:
            k = key.lower()
            k = k.replace(' ', '_')
            nkeys.append(k)
        return nkeys

    def __process_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.entries.append(row)
                if row.get('cluster'):
                    cluster = row['cluster']
                    if cluster not in self.clusters:
                        self.clusters.append(cluster)
                Console.print(row)
            self.entries_keys = list(self.entries[0].keys())
            self.keys = self.__normalize_keys(self.entries_keys)

    def __save_cluster_entries(self, cluster, entries):
        output_filename = self.args['--output-file']
        if output_filename == None:
            print("Use --output-file to specify output for entries of cluster: '{name}'".format(name=cluster))
            return -1
        with open(output_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar=' ',
                                    quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(self.keys)
            for e in entries:
                csv_writer.writerow(list(e.values()))
        print("Wrote '{size}' entries for cluster '{name}' in file: '{filename}'".format(size=len(entries), name=cluster, filename=output_filename))
        return 0

    def name(self):
      return "csv"

    def verify(self):
        filename = self.args['FILE']
        if not self.__check_file(filename): return -1
        self.__process_csv(filename)
        print("Entries:  found '{size}' entries in '{filename}'".format(size=len(self.entries), filename=filename))
        print("Keys:     found '{size}' keys: {keys}".format(size=len(self.keys), keys=', '.join(self.keys)))
        print("Clusters: found '{size}' clusters: {clusters}".format(size=len(self.clusters), clusters=', '.join(self.clusters)))
        return 0

    def split(self):
        cluster = self.args['CLUSTER']
        filename = self.args['FILE']
        if not self.__check_file(filename): return -1
        self.__process_csv(filename)
        if cluster in self.clusters:
            cluster_entries = []
            for e in self.entries:
                if e['cluster'] == cluster:
                    cluster_entries.append(e)
        print("Found '{size}' entries for '{name}' cluster".format(size=len(cluster_entries), name=cluster))
        return self.__save_cluster_entries(cluster, cluster_entries)
