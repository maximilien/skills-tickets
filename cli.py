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

import yaml

class CLI:
    def __init__(self, args):
        self.args = args
        self.__setup_credentials()

    def __parse_credentials(self):
        self.credentials = {}
        file_name = self.args['--credentials']
        if file_name:
            try:
                with open(file_name) as file:
                    self.credentials = yaml.load(file, Loader=yaml.FullLoader)
            except:
                print("Error opening credentials file: {file_name}".format(file_name=file_name))
        return self.credentials

    def __setup_credentials(self):
        self.credentials = self.__parse_credentials()
        if self.args['--api-key'] and self.args['--credentials']:
            print("WARNING: using --api-key value in credentials")
            self.credentials['api-key'] = self.args['--api-key']

        if self.args['--api-secret'] and self.args['--credentials']:
            print("WARNING: using --api-secret value in credentials")
            self.credentials['api-secret'] = self.args['--api-secret']

        if self.args['--subdomain'] and self.args['--credentials']:
            print("WARNING: using --subdomain value in credentials")
            self.credentials['subdomain'] = self.args['--subdomain']

    def command(self):
        if self.args.get('tickets') and self.args['tickets']:
            return Tickets(self.args)
        elif self.args.get('suggestions') and self.args['suggestions']:
            return Suggestions(self.args)
        else:
            raise Exception("Invalid command")

class Command:
    def __init__(self, args):
        self.args = args

    def execute(self):
        func = self.dispatch()
        try:
            rc = func()
            if rc == None:
                return 0
            else:
                if isinstance(rc, int):
                    return rc
                else:
                    return -1
        except Exception as e:
            print("LOG: error {message}".format(message=e.message))
            return -1
        except:
            print("LOG: unknown error {message}".format(message=e.message))
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
        else:
            raise Exception("Invalid subcommand")

# tickets command group
class Tickets(Command):
    def __init__(self, args):
        self.args = args
        super().__init__(self.args)

    def name(self):
        return "tickets"

    def list(self):
      print("tickets list: {--subdomain} {--api-key} {--api-secret}".format(**self.args))

    def show(self):
      print("tickets show: {ID} {--subdomain} {--api-key} {--api-secret}".format(**self.args))

    def delete(self):
      print("tickets delete: {ID} {--subdomain} {--api-key} {--api-secret}".format(**self.args))

    def create(self):
      print("tickets create: {TITLE} {BODY} {--subdomain} {--api-key} {--api-secret}".format(**self.args))

# suggestions command group
class Suggestions(Command):
    def __init__(self, args):
        self.args = args
        super().__init__(self.args)

    def name(self):
        return "suggestions"

    def list(self):
      print("suggestions list: {--subdomain} {--api-key} {--api-secret}".format(**self.args))

    def show(self):
      print("suggestions show: {ID} {--subdomain} {--api-key} {--api-secret}".format(**self.args))

    def delete(self):
      print("tickets delete: {ID} {--subdomain} {--api-key} {--api-secret}".format(**self.args))

    def create(self):
      print("suggestions create: {TICKET-ID} {TITLE} {BODY} {--subdomain} {--api-key} {--api-secret}".format(**self.args))
