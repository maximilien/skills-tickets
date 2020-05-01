#!/usr/bin/env bash

# Copyright 2020 IBM
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

export PATH=$PWD:$PATH

dir=$(dirname "${BASH_SOURCE[0]}")
base=$(cd "$dir/.." && pwd)
kn_path=`which python3`

# Start testing
echo "🧪  Testing"
kn_path -m unittest ${base}/test/*_e2e_test.py "$@"

# Output
echo ""
if [ $? -eq 0 ]; then
   echo "✅ Success"
else
	echo "❗️Failure"
fi
