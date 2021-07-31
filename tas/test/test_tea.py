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
from proclets.types import Init
from proclets.types import Exit
from proclets.types import Termination

from tas.tea import Brew
from tas.tea import Kit
from tas.tea import Maturity
from tas.tea import Tidy
from tas.tea import promise_tea


class MaturityTests(unittest.TestCase):

    def test_init(self):
        state = Maturity.inception
        self.assertEqual(state, state.trigger())
        self.assertEqual(Maturity.elaboration, state.trigger(Init.request))

class TypeTests(unittest.TestCase):

    def test_tallies(self):
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

        self.assertEqual(1, p.tally["pro_missing"])
        self.assertGreater(p.tally["pro_inspecting"], 1)
        created = [v for k, v in Proclet.population.items() if k not in baseline]
        totals = Counter(type(i) for i in created)
        for cls, n in totals.items():
            with self.subTest(cls=cls):
                self.assertEqual(Counter({Brew: 1, Kit: 5, Tidy: 2})[cls], totals[cls])

        for cls in (Kit, Tidy):
            for p in created:
                if isinstance(p, cls):
                    with self.subTest(p=p):
                        self.assertTrue(all(i == 1 for i in p.tally.values()))

