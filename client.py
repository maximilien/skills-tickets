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
        print("create_sso: {display_name}, {email}, {valid_time}".format(display_name=self.credentials.display_name(), email=self.credentials.email(), valid_time=valid_time))
        return uservoice.generate_sso_token(self.credentials.subdomain(), 
                                            self.credentials.sso_key(), {
                                            'email': self.credentials.email()
                                            }, valid_time*60)

    def get_client(self):
        if self.client == None:
            self.client = uservoice.Client(self.credentials.subdomain(), 
                                           self.credentials.api_key(), 
                                           self.credentials.api_secret(), 
                                           callback=self.credentials.url_callback())
        return self.client

    # Suggestions
    def get_suggestions(self):
        return self.get_client().get_collection("/api/v1/suggestions?sort=newest")

    def get_suggestion(self, id):
        return self.get_client().get("/api/v1/suggestions/{id}".format(id=id))['suggestion']

    def post_suggestion(self, forum_id, title, text):
        with self.get_client().login_as(self.credentials.email()) as access_token:
            suggestion = access_token.post("/api/v1/forums/{forum_id}/suggestions.json".format(forum_id=forum_id), {
                'email': self.credentials.email(),
                'suggestion': {
                    'title': title,
                    'text': text
                }
            })['suggestion']
            return suggestion

    def put_delete_ticket(self, id):
        return self.get_client().put("/api/v1/suggestions/{id}/delete".format(id=id))

    # Tickets
    def get_tickets(self):
        # return self.get_client().get_collection("/api/v1/tickets?sort=newest")
        with self.get_client().login_as(self.credentials.email()) as access_token:
            return access_token.get_collection("/api/v1/tickets?sort=newest")
        return []

    def get_ticket(self, id):
        return self.get_client().get("/api/v1/tickets/", {'id': id})['tickets'][0]

    def post_ticket(self, email, subject, message):
        question = self.get_client().post("/api/v1/tickets.json", {
            'email': email,
            'ticket': {
                'subject': subject,
                'message': message
            }
        })['ticket']
        return question

    def put_delete_ticket(self, id):
        return self.get_client().put("/api/v1/tickets/{id}/delete".format(id=id))

    # Forums
    def get_forums(self):
        return self.get_client().get_collection("/api/v1/forums?sort=newest")

    def get_forum(self, id):
        return self.get_client().get("/api/v1/forums/", {'id': id})['forums'][0]

