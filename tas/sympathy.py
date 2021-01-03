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

from turberfield.dialogue.model import SceneScript

from tas.tea import Acting
from tas.tea import TeaTime
from tas.types import Character


class TeaAndSympathy(TeaTime):

    @property
    def folder(self):
        return SceneScript.Folder(
            pkg="tas.dlg",
            description="Tea and Sympathy",
            metadata={},
            paths=["early.rst", "kettle.rst", "thanks.rst", "weblinks.rst"],
            interludes=None
        )

    def build(self):
        yield from super().build()
        yield from [
            Character(names=["Sophie"]).set_state(Acting.passive),
            Character(names=["Louise"]).set_state(Acting.active),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_quit)

    def do_quit(self, this, text, /, **kwargs):
        """
        exit | finish | stop | quit

        """
        for i in self.ensemble:
            if isinstance(i, Character):
                i.state = Acting.passive
        yield ""
        print(self.lookup)
