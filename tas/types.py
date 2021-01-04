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

import random

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import Stateful

class Named(DataObject):

    @property
    def name(self):
        return random.choice(getattr(self, "names", []))

class Character(Named, Stateful): pass

class Similar(Stateful):

    """An object which derives its state from another. """

    def __init__(self, other=None, **kwargs):
        super().__init__(**kwargs)
        self.other = other or self

    def get_state(self, **kwargs):
        return self.other.get_state(**kwargs)


