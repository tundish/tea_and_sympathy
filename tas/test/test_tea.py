#!/usr/bin/env python3
# encoding: utf-8

# This is a technical demo and teaching example for the turberfield-catchphrase library.
# Copyright (C) 2021 D E Haynes

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


from collections import Counter
import unittest
import uuid

from proclets.proclet import Proclet
from proclets.types import Termination

from tas.tea import promise_tea


class TypeTests(unittest.TestCase):

    def test_construct(self):
        baseline = set(Proclet.population.keys())
        p = promise_tea()
        self.assertFalse(p.intent)
        self.assertFalse(p.result)
        while True:
            try:
                r = list(p(mugs=2, tea=2, milk=2, spoons=1, sugar=1))
            except Termination:
                self.assertTrue(p.result)
                break

        created = [v for k, v in Proclet.population.items() if k not in baseline]
        self.assertTrue(created)
