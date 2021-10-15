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

import bisect
from collections import Counter
from collections import defaultdict
from collections import namedtuple
import functools
import itertools
import random
import re
import textwrap

from proclets.tea import execute
from proclets.tea import promise
from turberfield.catchphrase.parser import CommandParser
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.utils.misc import group_by_type

from tas.drama import Drama
from tas.types import Article
from tas.types import Availability
from tas.types import Character
from tas.types import Consumption
from tas.types import Container
from tas.types import Facility
from tas.types import Interaction
from tas.types import Journey
from tas.types import Location
from tas.types import Motivation
from tas.types import Name
from tas.types import Operation
from tas.types import Phrase
from tas.types import Production
from tas.types import Pronoun
from tas.types import Verb

#TODO: balladeer.types, balladeer.speech
class Grouping(defaultdict):

    @property
    def all(self):
        return [i for s in self.values() for i in s]

    @property
    def each(self):
        return set(self.all)


class World:

    @property
    def facility(self):
        return {
            "{0.phrase.verb.imperative} {0.phrase.name.noun}".format(i): i for i in [
                Facility(phrase=Phrase(Verb("drink"), Name("tea")), interaction=Interaction.consume),
                Facility(phrase=Phrase(Verb("make"), Name("tea")), interaction=Interaction.produce),
                Facility(
                    phrase=Phrase(Verb("smoke", progressive="is smoking", perfect="smoked"), Name("cigarette")),
                    interaction=Interaction.consume
                ),
            ]
        }

    @property
    def local(self):
        reach = (self.player.location, Location.inventory)
        grouped = group_by_type(i for i in self.lookup.each if i.get_state(Location) in reach)
        return Grouping(list, {k.__name__: v for k, v in grouped.items()})

    @functools.cached_property
    def player(self):
        return next(
            i for s in self.lookup.values() for i in s
            if i.get_state(Motivation) == Motivation.player
        )

    @property
    def visible(self):
        return [
            i for s in self.lookup.values() for i in s
            if i.get_state(Availability) != Availability.removed
        ]

    def __init__(self, *args, **kwargs):
        self.lookup = Grouping(list)
        for item in self.build():
            for n in item.names:
                self.lookup[n].append(item)

        self.promise = promise()
        self.flow = execute(self.promise, mugs=2, tea=2, milk=2, spoons=1, sugar=1)

    def build(self):
        return [
            Container(
                names=[Name("Mug")],
                description=textwrap.dedent(
                    """
                    A pale blue mug. It has on it a cartoon Teddy Bear
                    and the slogan 'I Fly Luton'.

                    It is dusted with ash. Inside are several cigarette butts.
                    They are crushed and soggy.

                    One however is almost pristine.
                    Only slightly charred and no trace of any lipstick.
                    
                    """,
                ),
                facility=self.facility["smoke cigarette"]
            ).set_state(Location.bedroom, Availability.removed),
            Container(
                names=[Name("Kettle")],
                description=textwrap.dedent(
                    """
                    A battered old kettle.

                    """,
                ),
                facility=self.facility["make tea"]
            ).set_state(Location.kitchen, Availability.removed),
            Character(
                names=[Name("Sophie", Article("", ""), Pronoun("she", "her", "herself", "hers"))],
                description="{0.name} goes to art college."
            ).set_state(Motivation.acting, Location.kitchen),
            Character(
                names=[Name("Louise", Article("", ""), Pronoun("she", "her", "herself", "hers"))],
                description="{0.name} is a young woman from Manchester. She works as a nurse."
            ).set_state(Motivation.player, Location.bedroom),
        ]
