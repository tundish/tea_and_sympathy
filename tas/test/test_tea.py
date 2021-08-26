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

from proclets.proclet import Proclet
from proclets.types import Init
from proclets.types import Exit
from proclets.types import Termination

from tas.tea import Brew
from tas.tea import Kit
from tas.tea import Fruition
from tas.tea import Tidy
from tas.tea import execute
from tas.tea import promise


class FlowTests(unittest.TestCase):

    def setUp(self):
        self.baseline = set(Proclet.population.keys())

    def test_tallies(self):
        p = promise()
        self.assertFalse(p.requests)
        self.assertFalse(p.result)
        list(execute(p, mugs=2, tea=2, milk=2, spoons=1, sugar=1))

        self.assertEqual(3, p.tally["pro_missing"])
        self.assertEqual(9, p.tally["pro_boiling"])
        self.assertEqual(6, p.tally["pro_inspecting"])
        created = [v for k, v in Proclet.population.items() if k not in self.baseline]
        totals = Counter(type(i) for i in created)
        for cls, n in totals.items():
            with self.subTest(cls=cls):
                self.assertEqual(Counter({Brew: 1, Kit: 5, Tidy: 2})[cls], totals[cls])

        for cls in (Kit, Tidy):
            for p in created:
                if isinstance(p, cls):
                    with self.subTest(p=p):
                        self.assertTrue(all(i == 1 for i in p.tally.values()))

    def test_promise_request(self):
        kit = None
        p = promise()
        for n, m in enumerate(execute(p, mugs=2, tea=2, milk=2, spoons=1, sugar=1)):

            if isinstance(m, Kit) and "mugs" in m.name:
                kit = m

            if n == 24:
                self.assertEqual(Fruition.construction, p.fruition[(("mugs", 2),)])
                self.assertEqual(Fruition.construction, kit.fruition[(("mugs", 2),)])

            elif n == 30:
                for c in ("mugs", "tea", "milk", "spoons", "sugar"):
                    self.assertIn(c, p.result)

            elif n == 46:
                self.assertEqual(Fruition.transition, p.fruition[(("mugs", 2),)])
                self.assertEqual(Fruition.transition, kit.fruition[(("mugs", 2),)])

            # Guard against injecting new jobs by accident
            self.assertTrue(all(len(i) == 2 for k, v in p.fruition.items() for i in k), p.fruition)

    def test_confirm_counter(self):
        """
        Brew -> Kit:    Can you get the mugs out for me?
        Kit -> Brew:    I'll get them in a minute.
        Brew -> Kit:    OK fine.

        """
        kit = None
        p = promise()
        p.actions.update({Init.counter: Init.confirm})
        for n, m in enumerate(execute(p, mugs=2, tea=2, milk=2, spoons=1, sugar=1)):
            if n > 60:
                break

            if isinstance(m, Kit) and "mugs" in m.name:
                kit = m
                kit.actions.update({Init.request: Init.counter})

            if n == 20:
                self.assertEqual(Fruition.discussion, p.fruition[(("mugs", 2),)])

            elif n == 21:
                self.assertEqual(Fruition.construction, p.fruition[(("mugs", 2),)])

            elif n == 31:
                self.assertEqual(Fruition.construction, p.fruition[(("mugs", 2),)])

            elif n == 36:
                for c in ("mugs", "tea", "milk", "spoons", "sugar"):
                    self.assertIn(c, p.result)

            elif n == 47:
                self.assertEqual(Fruition.transition, p.fruition[(("mugs", 2),)])

            # Guard against injecting new jobs by accident
            self.assertTrue(all(len(i) == 2 for k, v in p.fruition.items() for i in k), p.fruition)

    def test_decline_transition(self):
        """
        Brew -> Tidy:   Can you wash the mugs out for me?
        Tidy -> Brew:   There you go.
        Brew -> Tidy:   All of them, please.

        """
        tidy = None
        p = promise()
        p.actions.update({Init.counter: Init.confirm})
        for n, m in enumerate(execute(p, mugs=2, tea=2, milk=2, spoons=1, sugar=1)):
            if n > 65:
                print(p.result, p.result["mugs"])
                print(p.population[p.result.maps[0].uid])
                break

            print(n, p.fruition[(("mugs", 2),)])
            if isinstance(m, Tidy) and "mugs" in m.name:
                tidy = m

            if n == 40:
                tidy.requests[(("mugs", 1),)] = tidy.requests.pop((("mugs", 2),))  # TODO: Make a public method
                print(tidy.requests)

            # Guard against injecting new jobs by accident
            self.assertTrue(all(len(i) == 2 for k, v in p.fruition.items() for i in k), p.fruition)
