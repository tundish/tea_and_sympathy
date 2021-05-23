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


class MediatorTests(unittest.TestCase):

    def test_make_a_brew(self):
        mediator = TeaAndSympathy()
        for i in mediator.build():
            mediator.add(i)
        self.assertFalse(mediator.outcomes["brewed"])
        self.assertFalse(mediator.outcomes["stingy"])

        kettle = next(iter(mediator.lookup["kettle"]))
        fn, args, kwargs = mediator.interpret(mediator.match("put the kettle on"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        for n in range(30, 110, 10):
            with self.subTest(n=n):
                fn, args, kwargs = mediator.interpret(mediator.match("check the kettle"))
                dlg = "\n".join(mediator(fn, *args, **kwargs))
                self.assertEqual(n, kettle.state)
                self.assertEqual(
                    n,
                    next(i for i in kettle.contents(mediator.ensemble) if "water" in getattr(i, "names", [])).state
                )
                self.assertEqual(Location.hob, kettle.get_state(Location))

        self.assertEqual(2, len([i for i in mediator.ensemble if "water" in getattr(i, "names", [])]))

        fn, args, kwargs = mediator.interpret(mediator.match("find mug"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        mug = kwargs["obj"]
        self.assertEqual(Location.counter, mug.get_state(Location))
        self.assertTrue(mediator.outcomes["stingy"])

        fn, args, kwargs = mediator.interpret(mediator.match("pour water into the mug"))
        self.assertEqual(mediator.do_pour_liquid, fn, mediator.active)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        mug = kwargs["dst"]
        self.assertEqual(
            100,
            next(i for i in mug.contents(mediator.ensemble) if "water" in getattr(i, "names", [])).state
        )
        self.assertFalse(mediator.outcomes["brewed"])
        fn, args, kwargs = mediator.interpret(mediator.match("drop a teabag in the mug"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertTrue(mediator.outcomes["brewed"])

        self.assertTrue(mediator.outcomes["stingy"])
        fn, args, kwargs = mediator.interpret(mediator.match("pour some milk into the mug"))
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        self.assertFalse(mediator.outcomes["stingy"])

    def test_sugar_in_mug(self):
        mediator = TeaAndSympathy()
        for i in mediator.build():
            mediator.add(i)
        sugar = next(i for i in mediator.ensemble if "sugar" in i.names)
        fn, args, kwargs = mediator.interpret(mediator.match("find sugar"))
        self.assertTrue(fn)
        dlg = "\n".join(mediator(fn, *args, **kwargs))
        fn, args, kwargs = mediator.interpret(mediator.match("find mug"))
        mug = kwargs["obj"]
        self.assertFalse(mediator.outcomes["sugary"])
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
        self.assertTrue(mediator.outcomes["sugary"])


class DialogueTests(unittest.TestCase):

    def setUp(self):
        self.story = Story()
        self.mediator = self.story.mediator
        self.ensemble = self.mediator.ensemble + [self.mediator, Settings()]

    def test_early(self):
        next(iter(self.mediator.lookup["kettle"])).state = 20
        fn, args, kwargs = self.mediator.interpret(self.mediator.match("look"))
        data = self.mediator(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.mediator.folder, data, ensemble=self.ensemble)
        self.assertEqual("early.rst", self.mediator.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_kettle(self):
        next(iter(self.mediator.lookup["kettle"])).state = 20
        next(iter(self.mediator.lookup["hob"])).state = Motivation.acting
        fn, args, kwargs = self.mediator.interpret(self.mediator.match("look"))
        data = self.mediator(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.mediator.folder, data, ensemble=self.ensemble)
        self.assertEqual("kettle.rst", self.mediator.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_made(self):
        next(iter(self.mediator.lookup["kettle"])).state = 100
        mug = next(iter(self.mediator.lookup["mug"]))
        mug.state = Location.counter
        fn, args, kwargs = self.mediator.interpret(self.mediator.match("look"))
        data = self.mediator(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.mediator.folder, data, ensemble=self.ensemble)
        self.assertEqual("made.rst", self.mediator.folder.paths[presenter.index])
        self.assertTrue(presenter.frames[-1][Model.Line][-1].persona, vars(presenter))

    def test_pause(self):
        fn, args, kwargs = self.mediator.interpret(self.mediator.match("help"))
        data = self.mediator(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.mediator.folder, data, ensemble=self.ensemble)
        self.assertEqual("pause.rst", self.mediator.folder.paths[presenter.index])
        self.assertIsInstance(presenter.frames[-1][Model.Line][-1].persona, TeaAndSympathy, vars(presenter))

    def test_quit(self):
        fn, args, kwargs = self.mediator.interpret(self.mediator.match("quit"))
        data = self.mediator(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.mediator.folder, data, ensemble=self.ensemble)
        self.assertEqual("quit.rst", self.mediator.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona, vars(presenter))


class FuzzTests(unittest.TestCase):

    def test_random_walk(self):
        story = Story()
        ensemble = story.mediator.ensemble + [story.mediator, Settings()]
        for i in range(64):
            commands = {
                cmd for fn in story.mediator.active for cmd, _ in CommandParser.expand_commands(fn, ensemble=ensemble)
            }
            self.assertIn("help", commands)
            self.assertIn("history", commands)
            command = random.choice(list(commands))
            fn, args, kwargs = story.mediator.interpret(story.mediator.match(command))
            result = story.mediator(fn, *args, **kwargs)
            print(result)
            presenter = story.represent(result)
            with self.subTest(i=i, command=command):
                self.assertTrue(presenter, story.mediator.history)
            for frame in presenter.frames:
                animation = presenter.animate(frame, dwell=presenter.dwell, pause=presenter.pause)
                if not animation:
                    continue
                list(story.render_frame_to_terminal(animation))
