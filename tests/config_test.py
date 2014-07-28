#!/usr/bin/python
#
# Copyright 2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
#
# Tests handling of VM images (e.g., shortnames).

import json
import os
import unittest

# Local imports
import config


class ConfigExpanderTest(unittest.TestCase):

  def _FileBasename(self, filename):
    base1 = os.path.splitext(filename)[0]
    return os.path.splitext(base1)[0]

  def testFileBasename(self):
    before_after = (
        ('abc.in.yaml', 'abc'),
        ('foo.out.json', 'foo'),
    )
    for before, after in before_after:
      self.assertEqual(after, self._FileBasename(before))

  def testAllFiles(self):
    all_files = os.listdir(os.path.join(os.path.dirname(__file__), 'testdata'))
    unique_files = sorted(set(map(lambda x: self._FileBasename(x), all_files)))
    for filename in unique_files:
      expected = 'testdata/%s.out.json' % filename
      with open(expected) as expected_in:
        expected_json = json.loads(expected_in.read(), encoding='utf-8')

      input_file = 'testdata/%s.in.yaml' % filename
      expander = config.ConfigExpander(project='dummy-project', zone='dummy-zone')
      actual_json = expander.ExpandFile(input_file)

      self.assertEqual(expected_json, actual_json)


if __name__ == '__main__':
  unittest.main()