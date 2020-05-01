#!/usr/bin/env python3

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

"""Skills Tickets

Usage:
  st.py tickets list [options]
  st.py tickets show ID [options]
  st.py tickets delete ID [options]
  st.py tickets create TITLE BODY [options]
  
  st.py suggestions list [options]
  st.py suggestions show ID [options]
  st.py suggestions delete ID [options]
  st.py suggestions create TICKET-ID TITLE BODY [options]
  
  st.py (-h | --help)
  st.py --version

Options:
  --credentials=FILE      A YAML file with subdomain, api-key, and api-secret.values.
  --subdomain=SUBDOMAIN   The subdomain name for this UserVoice installation [default: cognitiveclass].
  --email=EMAIL           The email for the current user.
  --api-key=API-KEY       The API key for the current user.
  --api-secret=API-SECRET The API key for the current user.
  -h --help               Show this screen.
  --version               Show version.

"""
import os, sys, traceback

from docopt import docopt
from cli import *

if __name__ == '__main__':
    args = docopt(__doc__, version='0.1')
    command = CLI(args).command()
    try:
      rc = command.execute()
      if rc != 0:
          sys.exit(rc)
    except:
        traceback.print_last()
        print("ERROR executing `{name}` command".format(name=command.name()))