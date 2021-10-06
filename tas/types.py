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

from collections import defaultdict
import enum
import random

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import Stateful


@enum.unique
class Motivation(enum.Enum):

    acting = 0
    player = 1


@enum.unique
class Operation(enum.Enum):

    begins = 0
    normal = 1
    paused = 2
    ending = 3
    finish = 4


@enum.unique
class Journey(enum.Enum):

    mentor = 0
    ordeal = 1
    reward = 2

class Named(DataObject):
    """

    See https://pypi.org/project/inflect/ for grammar support.

    """

    @property
    def name(self):
        return random.choice(getattr(self, "names", [""]))


class Component(Stateful):

    """An object which derives its state from another. """

    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent or self

    def get_state(self, typ=int, default=0):
        if self.parent is self:
            return super().get_state(typ, default)
        else:
            return self.parent.get_state(typ, default)


class Location(enum.Enum):

    bedroom = ["bedroom"]
    hall = ["hall", "hallway"]
    kitchen = ["kitchen"]
    stairs = ["stairs", "up", "up stairs", "upstairs"]


class Character(Named, Stateful):

    @property
    def locn(self):
        return self.get_state(Location).value[0]

class Feature(Named, Stateful): pass


class Space(Named, Stateful):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contents(self, ensemble):
        return [i for i in ensemble if getattr(i, "parent", None) is self]


class Liquid(Named, Component):

    @property
    def heat(self):
        if self.state <= 20:
            return "cold"
        elif self.state >= 60:
            return "hot"
        else:
            return "warm"


class Item(Named, Component): pass
class Mass(Named, Component): pass


class Drama:

    @property
    def ensemble(self):
        return list({i for s in self.lookup.values() for i in s})

    @property
    def turns(self):
        return len(self.history)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lookup = defaultdict(set)

    def build(self):
        return []

    def add(self, *args):
        for item in args:
            for n in getattr(item, "names", []):
                self.lookup[n].add(item)

    def play(self, cmd: str, context:dict) -> dict:
        fn, args, kwargs = self.interpret(self.match(cmd, context=context, ensemble=self.ensemble))
        return self(fn, *args, **kwargs)

    def interlude(self, folder, index, **kwargs) -> dict:
        return {}

