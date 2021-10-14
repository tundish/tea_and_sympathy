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
from collections import namedtuple
import enum
import random

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import Stateful

Article = namedtuple(
    "Article",
    ("definite", "indefinite"),
    defaults=("the", "a")
)
Pronoun = namedtuple(
    "Pronoun",
    ("subject", "object", "reflexive", "genitive"),
    defaults=("it", "it", "itself", "its")
)
Name = namedtuple(
    "Name",
    ("noun", "article", "pronoun"),
    defaults=("", Article(), Pronoun())
)

Tensed = namedtuple("Tensed", ("simple", "progressive", "perfect", "imperative"))

class Verb(Tensed):

    def __new__(cls, root, simple="{0}s", progressive="is {0}ing", perfect="{0}ed", imperative="{0}"):
        l = locals()
        return super().__new__(cls, *(l[i].format(root) for i in super()._fields))

Phrase = namedtuple("Phrase", ("verb", "name"))


class Motivation(enum.Enum):

    acting = enum.auto()
    player = enum.auto()


class Operation(enum.Enum):

    begins = enum.auto()
    frames = enum.auto()
    paused = enum.auto()
    prompt = enum.auto()
    ending = enum.auto()
    finish = enum.auto()


class Journey(enum.Enum):

    mentor = enum.auto()
    ordeal = enum.auto()
    reward = enum.auto()


class Availability(enum.Enum):

    allowed = enum.auto()
    removed = enum.auto()


class Named(DataObject):
    """

    See https://pypi.org/project/inflect/ for grammar support.

    """

    @property
    def name(self):
        name = random.choice(getattr(self, "names", [Name()]))
        article = name.article.definite and f"{name.article.definite} "
        return f"{article}{name.noun}"


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
    stairs = ["stairs", "stairway", "up", "up stairs", "upstairs"]
    inventory = None

    @property
    def label(self):
        return self.value[0]

    @property
    def title(self):
        return self.label.title()

    @property
    def options(self):
        topology = {
            Location.bedroom: [Location.hall],
            Location.hall: [Location.bedroom, Location.kitchen, Location.stairs],
            Location.kitchen: [Location.hall],
        }
        return topology.get(self, [])


class Located(Stateful):

    @property
    def location(self):
        return self.get_state(Location)


class Character(Named, Located):

    @property
    def location(self):
        return self.get_state(Location)


class Container(Named, Located): pass
class Feature(Named, Stateful): pass


# TODO: Keep local to TaS
class Consumption(enum.Enum):

    tea = Phrase(Verb("drink"), Name("tea"))
    cigarette = Phrase(Verb("smoke", progressive="is smoking", perfect="smoked"), Name("cigarette"))


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
