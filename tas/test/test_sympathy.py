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


class SympathyTests(unittest.TestCase):

    @staticmethod
    def turn(cmd, drama, settings, text=None):
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
        self.assertEqual(1, len([i for i in self.drama.ensemble if isinstance(i, Container)]))
        self.assertEqual(1, len([i for i in self.drama.local if isinstance(i, Container)]))
        presenter, animation, lines, text = self.turn("help", self.drama, self.settings)
        self.assertNotIn("mug", text.lower())

    def test_look(self):
        cmds = ["look"]
        text = None
        for n, cmd in enumerate(cmds):
            presenter, animation, lines, text = self.turn(cmd, self.drama, self.settings, text)

        self.assertIn("hall", text.lower())
        self.assertIn("mug", text.lower())
