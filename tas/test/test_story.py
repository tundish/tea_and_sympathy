#!/usr/bin/env python3
# encoding: utf-8

# This is a technical demo and teaching example for the turberfield-catchphrase library.
# Copyright (C) 2021 D. Haynes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest

from tas.story import Story


class StoryTests(unittest.TestCase):

    def test_timing(self):
        story = Story()
        self.assertEqual(0.3, story.dwell)        
        self.assertEqual(1.0, story.pause)        
