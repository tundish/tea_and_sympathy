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

import logging
import random
import sys
import unittest

from tas.story import Story
from tas.teatime import Motivation
from tas.teatime import Location
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
        fn, args, kwargs = self.drama.interpret(self.drama.match("look", ensemble=self.ensemble))
        data = self.drama(fn, *args, **kwargs)
        self.assertTrue(data)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("early.rst", self.drama.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_kettle(self):
        next(iter(self.drama.lookup["kettle"])).state = 20
        next(iter(self.drama.lookup["hob"])).state = Motivation.acting
        fn, args, kwargs = self.drama.interpret(self.drama.match("look", ensemble=self.ensemble))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("kettle.rst", self.drama.folder.paths[presenter.index])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona)

    def test_made(self):
        next(iter(self.drama.lookup["kettle"])).state = 100
        mug = next(iter(self.drama.lookup["mug"]))
        mug.state = Location.counter
        fn, args, kwargs = self.drama.interpret(self.drama.match("look", ensemble=self.ensemble))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("made.rst", self.drama.folder.paths[presenter.index])
        self.assertTrue(presenter.frames[-1][Model.Line][-1].persona, vars(presenter))

    def test_pause(self):
        fn, args, kwargs = self.drama.interpret(self.drama.match("help", ensemble=self.ensemble))
        data = self.drama(fn, *args, **kwargs)
        presenter = Presenter.build_presenter(self.drama.folder, data, self.drama.facts, ensemble=self.ensemble)
        self.assertEqual("pause.rst", self.drama.folder.paths[presenter.index], data)
        self.assertIsInstance(presenter.frames[-1][Model.Line][-1].persona, TeaAndSympathy, vars(presenter))

    def test_quit(self):
        fn, args, kwargs = self.drama.interpret(self.drama.match("quit", ensemble=self.ensemble))
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
            fn, args, kwargs = story.drama.interpret(story.drama.match(command, ensemble=ensemble))
            result = story.drama(fn, *args, **kwargs)
            presenter = story.represent(story.drama.facts)
            with self.subTest(i=i, command=command):
                self.assertTrue(presenter, story.drama.history)
            for frame in presenter.frames:
                animation = presenter.animate(frame, dwell=presenter.dwell, pause=presenter.pause)
                if not animation:
                    continue
                list(story.render_frame_to_terminal(animation))
import unittest

from collections import ChainMap
from collections import Counter
from types import SimpleNamespace
import uuid

from proclets.channel import Channel
from proclets.proclet import Proclet
from proclets.types import Init
from proclets.types import Exit
from proclets.types import Termination



class Construct(ChainMap):

    @classmethod
    def create(cls, uid=None, **kwargs):
        uid = uid or uuid.uuid4()
        return cls(uid, Counter(**kwargs))

    def __init__(self, uid, *maps):
        super().__init__(*maps)
        self.uid = uid


class Brew(Proclet):

    @property
    def net(self):
        return {
            self.pro_filling: [self.pro_boiling, self.pro_missing],
            self.pro_missing: [self.pro_claiming, self.pro_missing],
            self.pro_boiling: [self.pro_brewing],
            self.pro_claiming: [self.pro_inspecting, self.pro_claiming],
            self.pro_inspecting: [self.pro_approving],
            self.pro_approving: [self.pro_brewing],
            self.pro_brewing: [self.pro_serving],
            self.pro_serving: [],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(self.name)

    def pro_filling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_missing(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_boiling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_claiming(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_inspecting(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_approving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_brewing(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_serving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        raise Termination()
        yield


class Kit(Proclet):

    @property
    def net(self):
        return {
            self.pro_missing: [self.pro_finding],
            self.pro_finding: [self.pro_claiming],
            self.pro_claiming: [],
        }

    def pro_missing(self, this, **kwargs):
        yield

    def pro_finding(self, this, **kwargs):
        yield

    def pro_claiming(self, this, **kwargs):
        yield


class Tidy(Proclet):

    @property
    def net(self):
        return {
            self.pro_inspecting: [self.pro_cleaning],
            self.pro_cleaning: [self.pro_approving],
            self.pro_approving: [],
        }

    def pro_inspecting(self, this, **kwargs):
        yield

    def pro_cleaning(self, this, **kwargs):
        yield

    def pro_approving(self, this, **kwargs):
        yield


class TypeTests(unittest.TestCase):

    def test_construct(self):
        c = Construct.create()
        self.assertIsInstance(c.uid, uuid.UUID)

if __name__ == "__main__":
    logging.basicConfig(
        style="{", format="{proclet.name:>16}|{funcName:>14}|{message}",
        level=logging.DEBUG,
    )
    channels = {"public": Channel()}
    b = Brew.create(name="brew_tea", channels=channels)
    rv = None
    while rv is None:
        try:
            for m in b():
                logging.debug(m, extra={"proclet": b})
        except Termination:
            rv = 0
        except Exception:
            rv = 1

    sys.exit(rv)
