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

import random
import unittest

from tas.story import Story
from tas.tea import Motivation
from tas.tea import Location
from tas.sympathy import TeaAndSympathy

from turberfield.catchphrase.parser import CommandParser
from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import Model


class DramaTests(unittest.TestCase):

    def test_make_a_brew(self):
        drama = TeaAndSympathy()
        for i in drama.build():
            drama.add(i)
        self.assertFalse(drama.outcomes["brewed"])
        self.assertFalse(drama.outcomes["stingy"])
        self.assertTrue(drama.lookup["mug"])

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
                self.assertEqual(Location.hob, kettle.get_state(Location))

        self.assertEqual(2, len([i for i in drama.ensemble if "water" in getattr(i, "names", [])]))

        fn, args, kwargs = drama.interpret(drama.match("find mug", drama.ensemble))
        self.assertIn("obj", kwargs, (fn, args, kwargs, drama.active, [i for i in drama.ensemble if "mug" in i.names]))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.counter, mug.get_state(Location))
        self.assertTrue(drama.outcomes["stingy"])

        fn, args, kwargs = drama.interpret(drama.match("pour water into the mug", drama.ensemble))
        self.assertEqual(drama.do_pour_liquid, fn, drama.active)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        mug = kwargs["dst"]
        self.assertEqual(
            100,
            next(i for i in mug.contents(drama.ensemble) if "water" in getattr(i, "names", [])).state
        )
        self.assertFalse(drama.outcomes["brewed"])
        fn, args, kwargs = drama.interpret(drama.match("drop a teabag in the mug", drama.ensemble))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(drama.outcomes["brewed"])

        self.assertTrue(drama.outcomes["stingy"])
        fn, args, kwargs = drama.interpret(drama.match("pour some milk into the mug", drama.ensemble))
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertFalse(drama.outcomes["stingy"])

    def test_sugar_in_mug(self):
        drama = TeaAndSympathy()
        for i in drama.build():
            drama.add(i)
        sugar = next(i for i in drama.ensemble if "sugar" in i.names)
        fn, args, kwargs = drama.interpret(drama.match("find sugar", drama.ensemble))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        fn, args, kwargs = drama.interpret(drama.match("find mug", drama.ensemble))
        mug = kwargs["obj"]
        self.assertFalse(drama.outcomes["sugary"])
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertIn(drama.do_pour_mass, drama.active)
        fn, args, kwargs = drama.interpret(drama.match("put sugar in the mug", drama.ensemble))
        self.assertTrue(fn, "\n".join(
            c for f in drama.active for c, (fn, args) in CommandParser.expand_commands(f, drama.ensemble)
        ))
        self.assertTrue(fn)
        dlg = "\n".join(drama(fn, *args, **kwargs))
        self.assertTrue(any("sugar" in getattr(i, "names", []) for i in mug.contents(drama.ensemble)))
        self.assertTrue(drama.outcomes["sugary"])


class DialogueTests(unittest.TestCase):

    def setUp(self):
        self.story = Story()
        self.drama = self.story.drama
        self.ensemble = self.drama.ensemble + [self.drama, Settings()]

    def test_early(self):
        next(iter(self.drama.lookup["kettle"])).state = 20
        fn, args, kwargs = self.drama.interpret(self.drama.match("look", self.ensemble))
        data = self.drama(fn, *args, **kwargs)
        self.assertTrue(data)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("early.rst", self.drama.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_kettle(self):
        next(iter(self.drama.lookup["kettle"])).state = 20
        next(iter(self.drama.lookup["hob"])).state = Motivation.acting
        fn, args, kwargs = self.drama.interpret(self.drama.match("look"))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("kettle.rst", self.drama.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_made(self):
        next(iter(self.drama.lookup["kettle"])).state = 100
        mug = next(iter(self.drama.lookup["mug"]))
        mug.state = Location.counter
        fn, args, kwargs = self.drama.interpret(self.drama.match("look"))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("made.rst", self.drama.folder.paths[presenter.index])
        self.assertTrue(presenter.frames[-1][Model.Line][-1].persona, vars(presenter))

    def test_pause(self):
        fn, args, kwargs = self.drama.interpret(self.drama.match("help"))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("pause.rst", self.drama.folder.paths[presenter.index], data)
        self.assertIsInstance(presenter.frames[-1][Model.Line][-1].persona, TeaAndSympathy, vars(presenter))

    def test_quit(self):
        fn, args, kwargs = self.drama.interpret(self.drama.match("quit"))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, ensemble=self.ensemble)
        self.assertEqual("quit.rst", self.drama.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona, vars(presenter))


class FuzzTests(unittest.TestCase):

    def test_random_walk(self):
        story = Story()
        ensemble = story.drama.ensemble + [story.drama, Settings()]
        for i in range(64):
            commands = {
                cmd for fn in story.drama.active for cmd, _ in CommandParser.expand_commands(fn, ensemble=ensemble)
            }
            self.assertIn("help", commands)
            self.assertIn("history", commands)
            command = random.choice(list(commands))
            fn, args, kwargs = story.drama.interpret(story.drama.match(command))
            result = story.drama(fn, *args, **kwargs)
            presenter = story.represent(story.drama.facts)
            with self.subTest(i=i, command=command):
                self.assertTrue(presenter, story.drama.history)
            for frame in presenter.frames:
                animation = presenter.animate(frame, dwell=presenter.dwell, pause=presenter.pause)
                if not animation:
                    continue
                list(story.render_frame_to_terminal(animation))
