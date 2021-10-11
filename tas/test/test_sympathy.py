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


class SympathyTests(unittest.TestCase):

    def setUp(self):
        self.settings = Settings()
        self.drama = Sympathy()

    def test_enter(self):
        self.assertEqual(3, len(self.drama.local), self.drama.local)

    def test_look(self):
        cmds = ["look"]
        text = None
        for cmd in cmds:
            presenter = Presenter.build_presenter(
                self.drama.folder, text, facts=self.drama.facts,
                ensemble=self.drama.ensemble + [self.drama, self.settings]
            )
            animations = (
                presenter.animate(
                    f, dwell=presenter.dwell, pause=presenter.pause
                ) for f in presenter.frames
            )
            animation = next(filter(None, animations))
            lines = list(Renderer.render_frame_to_terminal(animation))
            print(lines)
            text = self.drama.deliver(cmd, presenter=presenter)
