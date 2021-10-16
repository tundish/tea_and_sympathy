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

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings

from tas.sympathy import Sympathy
from tas.types import Container
from tas.types import Location
from tas.types import Name


class SympathyTests(unittest.TestCase):

    @staticmethod
    def turn(cmd, drama, settings, text=None, previous=None):
        drama.interlude(drama.folder, previous and previous.index, previous and previous.ensemble)
        presenter = Presenter.build_presenter(
            drama.folder, text, facts=drama.facts,
            ensemble=drama.ensemble + [drama, settings]
        )
        animations = (
            presenter.animate(
                f, dwell=presenter.dwell, pause=presenter.pause
            ) for f in presenter.frames
        )
        animation = next(filter(None, animations))
        lines = list(Renderer.render_frame_to_terminal(animation))
        text = drama.deliver(cmd, presenter=presenter)
        return presenter, animation, lines, text

    def setUp(self):
        self.settings = Settings()
        self.drama = Sympathy()

    def test_enter(self):
        self.assertEqual(2, len([i for i in self.drama.ensemble if isinstance(i, Container)]))
        self.assertEqual(1, len([i for i in self.drama.local if isinstance(i, Container)]))
        presenter, animation, lines, text = self.turn("help", self.drama, self.settings, text, previous=presenter)
        self.assertNotIn("mug", text.lower(), text)

    def test_look(self):
        cmds = ["look"]
        text = None
        presenter = None
        for n, cmd in enumerate(cmds):
            presenter, animation, lines, text = self.turn(cmd, self.drama, self.settings, text, previous=presenter)

        self.assertIn("hall", text.lower())
        self.assertIn("mug", text.lower())

    def test_get(self):
        cmds = ["look", "inspect mug", "get mug", "help"]
        text = None
        presenter = None
        mug = next(iter(self.drama.world.lookup["mug"]))
        for n, cmd in enumerate(cmds):

            with self.subTest(n=n, cmd=cmd, phase="pre"):
                if n == 0:
                    self.assertNotIn(self.drama.do_get, self.drama.active)

            presenter, animation, lines, text = self.turn(cmd, self.drama, self.settings, text, previous=presenter)

            with self.subTest(n=n, cmd=cmd, phase="post"):
                if n == 0:
                    self.assertIn(self.drama.do_get, self.drama.active)
                elif n == 1:
                    self.assertIn("Luton", text, self.drama.world.visible.each)
                elif n == 2:
                    self.assertEqual(Location.inventory, mug.get_state(Location), text)

    def test_go(self):
        cmds = ["go hall", "go bedroom", "go hall", "go stairs", "go kitchen", "go hall", "go bedroom"]
        text = None
        presenter = None
        for n, cmd in enumerate(cmds):
            presenter, animation, lines, text = self.turn(cmd, self.drama, self.settings, text, previous=presenter)

            with self.subTest(n=n, cmd=cmd):
                self.assertIn(cmd.split()[-1], text.lower())

    def test_enter(self):
        self.assertIn("sophie", self.drama.world.lookup)
        self.assertIn("kettle", self.drama.world.lookup)
        self.assertIn("smoke cigarette", self.drama.world.lookup)
