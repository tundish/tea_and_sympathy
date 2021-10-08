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

import unittest

from tas.teatime import Motivation
from tas.teatime import Location
from tas.teatime import TeaTime

from turberfield.catchphrase.parser import CommandParser


class LocationTests(unittest.TestCase):

    def test_prepositions_away(self):
        self.assertIn("out", Location.drawer.away)
        self.assertIn("off", Location.shelf.away)
        self.assertIn("down from", Location.shelf.away)

    def test_prepositions_into(self):
        self.assertIn("in", Location.drawer.into)
        self.assertIn("on", Location.shelf.into)
        self.assertIn("up on", Location.shelf.into)


@unittest.skip("Refactoring")
class TeaTests(unittest.TestCase):

    def test_initial(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        self.assertTrue(drama.active)
        self.assertTrue("look" in "".join([i.__doc__ for i in drama.active]))
        kettle = next(i for i in drama.ensemble if "kettle" in i.names)
        self.assertEqual(20, kettle.state)
        tap = next(i for i in drama.ensemble if "tap" in i.names)
        self.assertEqual(20, tap.state)

    def test_examine_drawer(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        options = list(drama.match("examine drawer", ensemble=list(Location)))
        fn, args, kwargs = drama.interpret(options)
        self.assertTrue(fn)
        dlg = drama(fn, *args, **kwargs)
        self.assertIn("Spoons", dlg)

    def test_examine_hob(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        options = list(drama.match("examine hob", ensemble=list(Location)))
        fn, args, kwargs = drama.interpret(options)
        self.assertTrue(fn)
        dlg = drama(fn, *args, **kwargs)
        self.assertIn("Kettle", dlg)
        self.assertEqual(3, len(list(filter(None, dlg.splitlines()))), dlg)

    def test_examine_kettle_empty(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        options = list(drama.match("examine kettle", ensemble=drama.ensemble))
        fn, args, kwargs = drama.interpret(options)
        self.assertTrue(fn)
        dlg = drama(fn, *args, **kwargs)
        self.assertIn("kettle", dlg)
        self.assertEqual(2, len(dlg.splitlines()), dlg)

    def test_examine_kettle_filled(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        fn, args, kwargs = drama.interpret(drama.match("fill kettle with water", ensemble=drama.ensemble))
        dlg = "\n".join(drama(fn, *args, **kwargs))

        options = list(drama.match("examine kettle", ensemble=drama.ensemble))
        fn, args, kwargs = drama.interpret(options)
        self.assertTrue(fn)
        dlg = drama(fn, *args, **kwargs)
        self.assertIn("kettle", dlg)
        self.assertEqual(4, len(dlg.splitlines()), dlg)

    def test_cold_water_in_mug(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        fn, args, kwargs = drama.interpret(drama.match("find mug", ensemble=drama.ensemble))
        self.assertIn("obj", kwargs, kwargs)
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertIn(drama.do_pour_liquid, drama.active)
        fn, args, kwargs = drama.interpret(drama.match("pour water in the mug", ensemble=drama.ensemble))
        self.assertEqual(drama.do_pour_liquid, fn, drama.active)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        water = kwargs["src"]
        self.assertFalse(any("water" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))

    def test_milk_in_mug(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        fn, args, kwargs = drama.interpret(drama.match("find spoon", ensemble=drama.ensemble))
        self.assertTrue(fn)
        spoon = kwargs["obj"]
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertEqual(Location.counter, spoon.get_state(Location))

        milk = next(i for i in drama.ensemble if "milk" in i.names)
        fn, args, kwargs = drama.interpret(drama.match("find milk", ensemble=drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))

        fn, args, kwargs = drama.interpret(drama.match("find mug", ensemble=drama.ensemble))
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertEqual(Location.counter, mug.get_state(Location))

        fn, args, kwargs = drama.interpret(drama.match("stir milk", ensemble=drama.ensemble))
        self.assertFalse(fn)

        fn, args, kwargs = drama.interpret(drama.match("pour milk in the mug", ensemble=drama.ensemble))
        self.assertEqual(drama.do_pour_liquid, fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(any("milk" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))

        fn, args, kwargs = drama.interpret(drama.match("stir milk", ensemble=drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))

    def test_sugar_in_mug(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        sugar = next(i for i in drama.ensemble if "sugar" in i.names)
        fn, args, kwargs = drama.interpret(drama.match("find sugar", ensemble=drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        fn, args, kwargs = drama.interpret(drama.match("find mug", ensemble=drama.ensemble))
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertIn(drama.do_pour_mass, drama.active)
        fn, args, kwargs = drama.interpret(drama.match("put sugar in the mug", ensemble=drama.ensemble))
        self.assertTrue(fn, "\n".join(
            c for f in drama.active for c, (fn, args) in CommandParser.expand_commands(f, drama.ensemble)
        ))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(any("sugar" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))

    def test_no_cold_water_in_mug(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        water = next(i for i in drama.ensemble if "water" in i.names)
        fn, args, kwargs = drama.interpret(drama.match("find mug", ensemble=drama.ensemble))
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertIn(drama.do_pour_liquid, drama.active)
        fn, args, kwargs = drama.interpret(drama.match("put tea in the mug", ensemble=drama.ensemble))
        self.assertTrue(fn, "\n".join(
            c for f in drama.active for c, (fn, args) in CommandParser.expand_commands(f, drama.ensemble)
        ))
        self.assertTrue(fn)
        self.assertEqual(drama.do_drop_item, fn)
        tea = kwargs["src"]
        mug = kwargs["dst"]
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(any("teabag" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))
        fn, args, kwargs = drama.interpret(drama.match("pour water in the mug", ensemble=drama.ensemble))
        self.assertEqual(drama.do_pour_liquid, fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertFalse(any("water" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))

    def test_disallowed(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        fn, args, kwargs = drama.interpret(drama.match("find a mug", ensemble=drama.ensemble))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.counter, mug.get_state(Location))
        for n, cmd in enumerate([
            "put hob in kettle",
        ]):
            with self.subTest(cmd=cmd, n=n):
                fn, args, kwargs = drama.interpret(drama.match(cmd))
                self.assertFalse(fn, kwargs)

    def test_kettle_one_step(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        hob = next(iter(drama.lookup["hob"]))
        kettle = next(iter(drama.lookup["kettle"]))
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(drama.ensemble))
        fn, args, kwargs = drama.interpret(drama.match("put the kettle on"))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(kettle.contents(drama.ensemble))
        self.assertTrue(Motivation.acting, hob.get_state(Motivation))

    def test_kettle_two_step(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        hob = next(i for i in drama.ensemble if "hob" in i.names)
        kettle = next(i for i in drama.ensemble if "kettle" in i.names)
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(drama.ensemble))
        fn, args, kwargs = drama.interpret(drama.match("fill the kettle", ensemble=drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertEqual(kettle.state, 20)
        self.assertTrue(kettle.contents(drama.ensemble))
        fn, args, kwargs = drama.interpret(drama.match("boil the kettle", ensemble=drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(kettle.contents(drama.ensemble))
        self.assertTrue(Motivation.acting, hob.get_state(Motivation))

    def test_make_a_brew(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        hob = next(iter(drama.lookup["hob"]))
        kettle = next(iter(drama.lookup["kettle"]))
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(drama.ensemble))
        fn, args, kwargs = drama.interpret(drama.match("put the kettle on", ensemble=drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(kettle.contents(drama.ensemble))
        self.assertTrue(Motivation.acting, hob.get_state(Motivation))
        for n in range(30, 110, 10):
            with self.subTest(n=n):
                fn, args, kwargs = drama.interpret(drama.match("check the kettle", ensemble=drama.ensemble))
                dlg = "\n".join(drama(fn, *args, **kwargs))
                self.assertEqual(n, kettle.state)

        fn, args, kwargs = drama.interpret(drama.match("find a mug", ensemble=drama.ensemble))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.counter, mug.get_state(Location))
        for n, cmd in enumerate([
            "find some tea", "put teabag in mug", "pour hot water into mug",
            "find spoon", "stir tea", "put the teabag in the bin"
        ]):
            with self.subTest(cmd=cmd, n=n):
                self.assertIn(drama.do_find, drama.active)
                options = list(drama.match(cmd, ensemble=drama.ensemble))
                fn, args, kwargs = drama.interpret(options)
                self.assertTrue(fn, "\n".join(
                    c for f in drama.active
                    for c, (fn, args) in CommandParser.expand_commands(f, drama.ensemble)
                ))
                dlg = "\n".join(drama(fn, *args, **kwargs))

        bin_ = next(iter(drama.lookup["bin"]))
        self.assertFalse(any("teabag" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))
        self.assertEqual(100, mug.state, drama.lookup["mug"])

        teabag = next((i for i in bin_.contents(drama.ensemble) if "teabag" in getattr(i, "names", [])), None)
        self.assertTrue(teabag)
        self.assertEqual(bin_.state, teabag.state)

    def test_full_story(self):
        drama = TeaTime()
        for i in drama.build():
            drama.add(i)
        kettle = next(iter(drama.lookup["kettle"]))
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(drama.ensemble))
        for cmd in [
            "get a mug", "put the kettle on",
            "find some tea", "put the teabag in the mug",
            "get a spoon", "get the milk",
            "get some sugar", "put the sugar in the mug",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIn(drama.do_find, drama.active)
                options = list(drama.match(cmd, ensemble=drama.ensemble))
                fn, args, kwargs = drama.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(drama(fn, *args, **kwargs))
                mugs = [i for i in drama.lookup["mug"] if i.get_state(Location) == Location.counter]
                self.assertEqual(1, len(mugs))

        self.assertEqual(80, kettle.state)
        fn, args, kwargs = drama.interpret(drama.match("check the kettle", ensemble=drama.ensemble))
        list(drama(fn, *args, **kwargs))
        list(drama(fn, *args, **kwargs))
        self.assertEqual(100, kettle.state)

        for cmd in [
            "pour water into the mug",
            "stir the tea",
            "put the teabag in the bin",
            "add the milk", "stir the tea",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIn(drama.do_find, drama.active)
                options = list(drama.match(cmd, ensemble=drama.ensemble))
                fn, args, kwargs = drama.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(drama(fn, *args, **kwargs))
                mugs = [i for i in drama.lookup["mug"] if i.get_state(Location) == Location.counter]
                self.assertEqual(1, len(mugs))

        self.assertFalse(any("teabag" in getattr(i, "names", []) for i in mugs[0].contents(drama.ensemble)))
        self.assertEqual(100, mugs[0].state, drama.lookup["mug"])

        bin_ = next(iter(drama.lookup["bin"]))
        teabag = next((i for i in bin_.contents(drama.ensemble) if "teabag" in getattr(i, "names", [])), None)
        self.assertTrue(teabag)
        self.assertEqual(bin_.state, teabag.state)
