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

import uservoice

class UserVoiceClient:
    def __init__(self, credentials):
        self.client = None
        self.credentials = credentials

    def __create_sso(self, valid_time=5):
        print("create_sso: {display_name}, {email}, {valid_time}".format(display_name=self.credentials.display_name, email=self.credentials.email, valid_time=valid_time))
        return uservoice.generate_sso_token(self.credentials.subdomain, 
                                            self.credentials.sso_key, {
                                                'email': email
                                            }, valid_time*60)

    def get_client(self):
        if self.client == None:
            self.client = uservoice.Client(self.credentials.subdomain(), 
                                           self.credentials.api_key(), 
                                           self.credentials.api_secret(), 
                                           callback=self.credentials.url_callback())
        return self.client

    def post_question(self, email, subject, message):
        question = self.get_client().post("/api/v1/tickets.json", {
            'email': email,
            'ticket': {
                'subject': subject,
                'message': message
            }
        })['ticket']
        return question

    def suggestions(self):
        return self.get_client().get_collection("/api/v1/suggestions?sort=newest")

    def suggestion(self, id):
        return self.get_client().get("/api/v1/suggestions/", {'id': id})['suggestions'][0]

    #     # Loads the first page (at most 100 records) of suggestions and reads the count.
    #     print('Total suggestions: {total}'.format(total=len(suggestions)))

    #     # Loops through all the suggestions and loads new pages as necessary.
    #     for suggestion in suggestions:
    #         print('{title}: {url}'.format(**suggestion))

    # def read_tickets(self, email):
    #     with self.get_client().login_as(email) as access_token:
    #         # Creates a lazy-loading collection object but makes no requests to the API yet.
    #         tickets = access_token.get_collection("/api/v1/tickets?sort=newest")

    #         # Loads the first page (at most 100 records) of suggestions and reads the count.
    #         print('Total tickets: {total}'.format(total=len(tickets)))

    #         # Loops through all the suggestions and loads new pages as necessary.
    #         for ticket in tickets:
    #             print('{id}: {ticket_number}'.format(**ticket))
