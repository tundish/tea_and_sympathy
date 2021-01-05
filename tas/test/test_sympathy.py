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

from tas.tea import Acting
from tas.tea import Location
from tas.sympathy import TeaAndSympathy

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import Model


class DramaTests(unittest.TestCase):

    def test_make_a_brew(self):
        drama = TeaAndSympathy()
        kettle = next(iter(drama.lookup["kettle"]))
        fn, args, kwargs = drama.interpret(drama.match("put the kettle on"))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        for n in range(30, 110, 10):
            with self.subTest(n=n):
                fn, args, kwargs = drama.interpret(drama.match("check the kettle"))
                dlg = "\n".join(drama(fn, *args, **kwargs))
                self.assertEqual(n, kettle.state)
                self.assertEqual(
                    n,
                    next(i for i in kettle.contents(drama.ensemble) if "water" in getattr(i, "names", [])).state
                )
                self.assertEqual(Location.HOB, kettle.get_state(Location))

        self.assertEqual(2, len([i for i in drama.ensemble if "water" in getattr(i, "names", [])]))

        fn, args, kwargs = drama.interpret(drama.match("find mug"))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.COUNTER, mug.get_state(Location))

        fn, args, kwargs = drama.interpret(drama.match("pour water in the mug"))
        self.assertEqual(drama.do_pour_liquid, fn, drama.active)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        mug = kwargs["dst"]
        self.assertEqual(
            100,
            next(i for i in mug.contents(drama.ensemble) if "water" in getattr(i, "names", [])).state
        )
        self.assertEqual(Location.COUNTER, mug.get_state(Location))
        self.assertEqual(Location.HOB, kettle.get_state(Location))


class DialogueTests(unittest.TestCase):

    def setUp(self):
        self.drama = TeaAndSympathy()
        self.ensemble = self.drama.ensemble + [self.drama, Settings()]

    def test_early(self):
        next(iter(self.drama.lookup["kettle"])).state = 20
        fn, args, kwargs = self.drama.interpret(self.drama.match("look"))
        results = list(self.drama(fn, *args, **kwargs))
        n, presenter = Presenter.build_from_folder(
            *Presenter.build_shots(*results, shot="Epilogue"),
            folder=self.drama.folder,
            ensemble=self.ensemble,
            strict=True
        )
        self.assertEqual("early.rst", self.drama.folder.paths[n])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_kettle(self):
        next(iter(self.drama.lookup["kettle"])).state = 20
        next(iter(self.drama.lookup["hob"])).state = Acting.active
        fn, args, kwargs = self.drama.interpret(self.drama.match("look"))
        results = list(self.drama(fn, *args, **kwargs))
        n, presenter = Presenter.build_from_folder(
            *Presenter.build_shots(*results, shot="Epilogue"),
            folder=self.drama.folder,
            ensemble=self.ensemble,
            strict=True
        )
        self.assertEqual("kettle.rst", self.drama.folder.paths[n])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_thanks(self):
        next(iter(self.drama.lookup["kettle"])).state = 100
        mug = next(iter(self.drama.lookup["mug"]))
        mug.state = Location.COUNTER
        fn, args, kwargs = self.drama.interpret(self.drama.match("look"))
        results = list(self.drama(fn, *args, **kwargs))
        n, presenter = Presenter.build_from_folder(
            *Presenter.build_shots(*results, shot="Epilogue"),
            folder=self.drama.folder,
            ensemble=self.ensemble,
            strict=True
        )
        self.assertEqual("thanks.rst", self.drama.folder.paths[n])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona, vars(presenter))

