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

from tas.tea import Motivation
from tas.tea import Location
from tas.tea import TeaTime

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


class TeaTests(unittest.TestCase):

    def test_initial(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        self.assertTrue(mediator.active)
        self.assertTrue("help" in "".join([i.__doc__ for i in mediator.active]))
        self.assertTrue("look" in "".join([i.__doc__ for i in mediator.active]))
        kettle = next(i for i in mediator.ensemble if "kettle" in i.names)
        self.assertEqual(20, kettle.state)
        tap = next(i for i in mediator.ensemble if "tap" in i.names)
        self.assertEqual(20, tap.state)

    def test_examine_drawer(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        options = list(mediator.match("examine drawer", ensemble=list(Location)))
        fn, args, kwargs = mediator.interpret(options)
        self.assertTrue(fn)
        dlg = mediator(fn, *args, **kwargs)
        self.assertIn("Spoons", dlg)

    def test_examine_hob(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        options = list(mediator.match("examine hob", ensemble=list(Location)))
        fn, args, kwargs = mediator.interpret(options)
        self.assertTrue(fn)
        dlg = mediator(fn, *args, **kwargs)
        self.assertIn("Kettle", dlg)
        self.assertEqual(3, len(dlg.splitlines()), dlg)

    def test_examine_kettle_empty(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        options = list(mediator.match("examine kettle", ensemble=list(Location)))
        fn, args, kwargs = mediator.interpret(options)
        self.assertTrue(fn)
        dlg = mediator(fn, *args, **kwargs)
        self.assertIn("kettle", dlg)
        self.assertEqual(2, len(dlg.splitlines()), dlg)

    def test_examine_kettle_filled(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        fn, args, kwargs = mediator.interpret(mediator.match("fill kettle with water"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))

        options = list(mediator.match("examine kettle", ensemble=list(Location)))
        fn, args, kwargs = mediator.interpret(options)
        self.assertTrue(fn)
        dlg = mediator(fn, *args, **kwargs)
        self.assertIn("kettle", dlg)
        self.assertEqual(4, len(dlg.splitlines()), dlg)

    def test_cold_water_in_mug(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        fn, args, kwargs = mediator.interpret(mediator.match("find mug"))
        self.assertIn("obj", kwargs, kwargs)
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertIn(mediator.do_pour_liquid, mediator.active)
        fn, args, kwargs = mediator.interpret(mediator.match("pour water in the mug"))
        self.assertEqual(mediator.do_pour_liquid, fn, mediator.active)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        water = kwargs["src"]
        self.assertFalse(any("water" in getattr(i, "names", []) for i in mug.contents(mediator.ensemble)))

    def test_milk_in_mug(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        fn, args, kwargs = mediator.interpret(mediator.match("find spoon"))
        self.assertTrue(fn)
        spoon = kwargs["obj"]
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertEqual(Location.counter, spoon.get_state(Location))

        milk = next(i for i in mediator.ensemble if "milk" in i.names)
        fn, args, kwargs = mediator.interpret(mediator.match("find milk"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))

        fn, args, kwargs = mediator.interpret(mediator.match("find mug"))
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertEqual(Location.counter, mug.get_state(Location))

        fn, args, kwargs = mediator.interpret(mediator.match("stir milk"))
        self.assertFalse(fn)

        fn, args, kwargs = mediator.interpret(mediator.match("pour milk in the mug"))
        self.assertEqual(mediator.do_pour_liquid, fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(any("milk" in getattr(i, "names", []) for i in mug.contents(mediator.ensemble)))

        fn, args, kwargs = mediator.interpret(mediator.match("stir milk"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))

    def test_sugar_in_mug(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        sugar = next(i for i in mediator.ensemble if "sugar" in i.names)
        fn, args, kwargs = mediator.interpret(mediator.match("find sugar"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        fn, args, kwargs = mediator.interpret(mediator.match("find mug"))
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertIn(mediator.do_pour_mass, mediator.active)
        fn, args, kwargs = mediator.interpret(mediator.match("put sugar in the mug"))
        self.assertTrue(fn, "\n".join(
            c for f in mediator.active for c, (fn, args) in CommandParser.expand_commands(f, mediator.ensemble)
        ))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(any("sugar" in getattr(i, "names", []) for i in mug.contents(mediator.ensemble)))

    def test_no_cold_water_in_mug(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        water = next(i for i in mediator.ensemble if "water" in i.names)
        fn, args, kwargs = mediator.interpret(mediator.match("find mug"))
        mug = kwargs["obj"]
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertIn(mediator.do_pour_liquid, mediator.active)
        fn, args, kwargs = mediator.interpret(mediator.match("put tea in the mug"))
        self.assertTrue(fn, "\n".join(
            c for f in mediator.active for c, (fn, args) in CommandParser.expand_commands(f, mediator.ensemble)
        ))
        self.assertTrue(fn)
        self.assertEqual(mediator.do_drop_item, fn)
        tea = kwargs["src"]
        mug = kwargs["dst"]
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(any("teabag" in getattr(i, "names", []) for i in mug.contents(mediator.ensemble)))
        fn, args, kwargs = mediator.interpret(mediator.match("pour water in the mug"))
        self.assertEqual(mediator.do_pour_liquid, fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertFalse(any("water" in getattr(i, "names", []) for i in mug.contents(mediator.ensemble)))

    def test_disallowed(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        fn, args, kwargs = mediator.interpret(mediator.match("find a mug"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.counter, mug.get_state(Location))
        for n, cmd in enumerate([
            "put hob in kettle",
        ]):
            with self.subTest(cmd=cmd, n=n):
                fn, args, kwargs = mediator.interpret(mediator.match(cmd))
                self.assertFalse(fn, kwargs)

    def test_kettle_one_step(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        hob = next(iter(mediator.lookup["hob"]))
        kettle = next(iter(mediator.lookup["kettle"]))
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(mediator.ensemble))
        fn, args, kwargs = mediator.interpret(mediator.match("put the kettle on"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(kettle.contents(mediator.ensemble))
        self.assertTrue(Motivation.acting, hob.get_state(Motivation))

    def test_kettle_two_step(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        hob = next(i for i in mediator.ensemble if "hob" in i.names)
        kettle = next(i for i in mediator.ensemble if "kettle" in i.names)
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(mediator.ensemble))
        fn, args, kwargs = mediator.interpret(mediator.match("fill the kettle"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertEqual(kettle.state, 20)
        self.assertTrue(kettle.contents(mediator.ensemble))
        fn, args, kwargs = mediator.interpret(mediator.match("boil the kettle"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(kettle.contents(mediator.ensemble))
        self.assertTrue(Motivation.acting, hob.get_state(Motivation))

    def test_make_a_brew(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        hob = next(iter(mediator.lookup["hob"]))
        kettle = next(iter(mediator.lookup["kettle"]))
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(mediator.ensemble))
        fn, args, kwargs = mediator.interpret(mediator.match("put the kettle on"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(kettle.contents(mediator.ensemble))
        self.assertTrue(Motivation.acting, hob.get_state(Motivation))
        for n in range(30, 110, 10):
            with self.subTest(n=n):
                fn, args, kwargs = mediator.interpret(mediator.match("check the kettle"))
                dlg = "\n".join(mediator(fn, *args, **kwargs))
                self.assertEqual(n, kettle.state)

        fn, args, kwargs = mediator.interpret(mediator.match("find a mug"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.counter, mug.get_state(Location))
        for n, cmd in enumerate([
            "find some tea", "put teabag in mug", "pour hot water into mug",
            "find spoon", "stir tea", "put the teabag in the bin"
        ]):
            with self.subTest(cmd=cmd, n=n):
                self.assertIn(mediator.do_find, mediator.active)
                options = list(mediator.match(cmd))
                fn, args, kwargs = mediator.interpret(options)
                self.assertTrue(fn, "\n".join(
                    c for f in mediator.active
                    for c, (fn, args) in CommandParser.expand_commands(f, mediator.ensemble)
                ))
                dlg = "\n".join(mediator(fn, *args, **kwargs))

        bin_ = next(iter(mediator.lookup["bin"]))
        self.assertFalse(any("teabag" in getattr(i, "names", []) for i in mug.contents(mediator.ensemble)))
        self.assertEqual(100, mug.state, mediator.lookup["mug"])

        teabag = next((i for i in bin_.contents(mediator.ensemble) if "teabag" in getattr(i, "names", [])), None)
        self.assertTrue(teabag)
        self.assertEqual(bin_.state, teabag.state)

    def test_full_story(self):
        mediator = TeaTime()
        for i in mediator.build():
            mediator.add(i)
        kettle = next(iter(mediator.lookup["kettle"]))
        self.assertEqual(20, kettle.state)
        self.assertFalse(kettle.contents(mediator.ensemble))
        for cmd in [
            "get a mug", "put the kettle on",
            "find some tea", "put the teabag in the mug",
            "get a spoon", "get the milk",
            "get some sugar", "put the sugar in the mug",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIn(mediator.do_find, mediator.active)
                options = list(mediator.match(cmd))
                fn, args, kwargs = mediator.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(mediator(fn, *args, **kwargs))
                mugs = [i for i in mediator.lookup["mug"] if i.get_state(Location) == Location.counter]
                self.assertEqual(1, len(mugs))

        self.assertEqual(80, kettle.state)
        fn, args, kwargs = mediator.interpret(mediator.match("check the kettle"))
        list(mediator(fn, *args, **kwargs))
        list(mediator(fn, *args, **kwargs))
        self.assertEqual(100, kettle.state)

        for cmd in [
            "pour water into the mug",
            "stir the tea",
            "put the teabag in the bin",
            "add the milk", "stir the tea",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIn(mediator.do_find, mediator.active)
                options = list(mediator.match(cmd))
                fn, args, kwargs = mediator.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(mediator(fn, *args, **kwargs))
                mugs = [i for i in mediator.lookup["mug"] if i.get_state(Location) == Location.counter]
                self.assertEqual(1, len(mugs))

        self.assertFalse(any("teabag" in getattr(i, "names", []) for i in mugs[0].contents(mediator.ensemble)))
        self.assertEqual(100, mugs[0].state, mediator.lookup["mug"])

        bin_ = next(iter(mediator.lookup["bin"]))
        teabag = next((i for i in bin_.contents(mediator.ensemble) if "teabag" in getattr(i, "names", [])), None)
        self.assertTrue(teabag)
        self.assertEqual(bin_.state, teabag.state)
