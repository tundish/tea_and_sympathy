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
from tas.tea import Fruition
from tas.tea import Tidy
from tas.tea import promise_tea


class FruitionTests(unittest.TestCase):

    def test_inception(self):
        state = Fruition.inception
        self.assertEqual(state, state.trigger())
        for i in Init:
            with self.subTest(state=state, i=i):
                if i == Init.request:
                    self.assertEqual(Fruition.elaboration, state.trigger(Init.request))
                else:
                    self.assertEqual(state, state.trigger(i))

    def test_elaboration(self):
        state = Fruition.elaboration
        for i in Init:
            with self.subTest(state=state, i=i):
                if i == Init.promise:
                    self.assertEqual(Fruition.construction, state.trigger(i))
                elif i in (Init.abandon, Init.decline):
                    self.assertEqual(Fruition.withdrawn, state.trigger(i))
                elif i == Init.counter:
                    self.assertEqual(Fruition.discussion, state.trigger(i))
                else:
                    self.assertEqual(state, state.trigger(i))

    def test_discussion(self):
        state = Fruition.discussion
        for i in Init:
            with self.subTest(state=state, i=i):
                if i == Init.counter:
                    self.assertEqual(Fruition.elaboration, state.trigger(i))
                elif i in (Init.abandon, Init.decline):
                    self.assertEqual(Fruition.withdrawn, state.trigger(i))
                elif i in (Init.confirm, Init.promise):
                    self.assertEqual(Fruition.construction, state.trigger(i))
                else:
                    self.assertEqual(state, state.trigger(i))

    def test_construction(self):
        state = Fruition.construction
        for i in Exit:
            with self.subTest(state=state, i=i):
                if i == Exit.deliver:
                    self.assertEqual(Fruition.transition, state.trigger(i))
                elif i == Exit.decline:
                    self.assertEqual(Fruition.moribund, state.trigger(i))
                elif i == Exit.abandon:
                    self.assertEqual(Fruition.cancelled, state.trigger(i))
                else:
                    self.assertEqual(state, state.trigger(i))

    def test_transition(self):
        state = Fruition.transition
        for i in Exit:
            with self.subTest(state=state, i=i):
                if i == Exit.decline:
                    self.assertEqual(Fruition.construction, state.trigger(i))
                elif i == Exit.abandon:
                    self.assertEqual(Fruition.cancelled, state.trigger(i))
                elif i == Exit.confirm:
                    self.assertEqual(Fruition.completion, state.trigger(i))
                else:
                    self.assertEqual(state, state.trigger(i))

    def test_terminal(self):
        for state in (
            Fruition.withdrawn, Fruition.moribund, Fruition.cancelled, Fruition.completion
        ):
            for i in list(Init) + list(Exit):
                with self.subTest(state=state, i=i):
                    self.assertEqual(state, state.trigger(i))


class FlowTests(unittest.TestCase):

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


    def test_acts(self):
        import sys
        baseline = set(Proclet.population.keys())
        p = promise_tea()
        n = 0
        while n < 100:
            try:
                for m in p(mugs=2, tea=2, milk=2, spoons=1, sugar=1):
                    if n == 0:
                        p.actions.update({Init.promise: Init.abandon})
                        p.contents.update({Init.promise: {"tea": 0}})
                    print(m, file=sys.stderr)
                    n += 1
            except Termination:
                print(n, file=sys.stderr)
                break
