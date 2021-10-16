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

from tas.drama import Drama
from tas.types import Article
from tas.types import Availability
from tas.types import Character
from tas.types import Consumption
from tas.types import Container
from tas.types import Gesture
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
from tas.world import World

from turberfield.catchphrase.mediator import Mediator
from turberfield.dialogue.types import Stateful


class Sympathy(Drama):

    @property
    def ensemble(self):
        return list(self.world.lookup.each)

    @property
    def folder(self):
        return SceneScript.Folder(
            pkg="tas.dlg",
            description="Tea and Sympathy",
            metadata={},
            paths=[
                "kitchen.rst", "enter.rst", # "funnel.rst",
                "paused.rst", "quit.rst"
                # "verdict"
            ],
            interludes=None
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = self.active.union({
            self.do_again, self.do_look,
            self.do_go, self.do_inspect,
            self.do_help, self.do_history, self.do_quit
        })
        self.default_fn = self.do_next

        self.set_state(Journey.mentor, Operation.prompt)
        self.world = World(*args, **kwargs)

    def interlude(self, folder, index, *args, **kwargs):
        return {}

    def do_again(self, this, text, presenter, *args, **kwargs):
        """
        again | back

        """
        n = len(list(itertools.takewhile(
            lambda x: x.name == this.__name__, self.history
        ))) + 1
        self.state = self.next_states(n)[0]
        return "again..."

    def do_consume(self, this, text, presenter, obj: "world.local.each", *args, **kwargs):
        """
        {obj.contents.value.verb.imperative} {obj.contents.value.name.noun}

        """
        # TODO: Remove consumption from container
        # TODO: Create a memory of subject=player, object=obj.contents, state=?
        self.world.player.state = obj.contents
        return obj.description.format(obj, **self.facts)

    def do_get(self, this, text, presenter, obj: "world.local[Container]", *args, **kwargs):
        """
        get {obj.names[0].noun}
        grab {obj.names[0].noun}
        take {obj.names[0].noun}
        pick up {obj.names[0].noun}

        """
        obj.state = Location.inventory
        self.active.discard(this)
        return f"{self.world.player.name} picks up {obj.names[0].article.definite} {obj.names[0].noun}.",

    def do_go(self, this, text, presenter, *args, locn: "world.player.location.options", **kwargs):
        """
        enter {locn.value[0]} | enter {locn.value[1]}
        go {locn.value[0]} | go {locn.value[1]} | go {locn.value[2]} | go {locn.value[3]} | go {locn.value[4]}

        """
        if locn == Location.stairs:
            yield f"{self.world.player.name} looks upward."
            yield "The stairs lead to an attic gallery, and Sophie's room."
            yield f"{self.world.player.name} hesitates."
            yield "She doesn't want to go up there."
        else:
            self.state = 0
            self.world.player.state = locn
            yield f"{self.world.player.name} goes into the {locn.title}."

    def do_help(self, this, text, presenter, *args, **kwargs):
        """
        help
        what | what do i do

        """
        self.state = Operation.paused
        options = {
            fn.__name__: list(CommandParser.expand_commands(fn, self.ensemble, parent=self))
            for fn in self.active
        }
        for k, v in sorted(options.items()):
            cmds = []
            for cmd, (fn, kwargs) in v:
                if all(isinstance(i, Location) or i in self.world.visible for i in kwargs.values()):
                    cmds.append(cmd)

            if cmds:
                yield "* {0}".format(random.choice(cmds))

    def do_history(self, this, text, presenter, *args, **kwargs):
        """
        history

        """
        self.state = Operation.paused
        yield from ("* {0.args[0]}".format(i) for i in self.history if i.args[0])

    def do_inspect(self, this, text, presenter, obj: "world.visible.each", *args, **kwargs):
        """
        inspect {obj.names[0].noun}

        """
        self.state = Operation.paused
        return obj.description.format(obj, **self.facts)

    def do_look(self, this, text, presenter, *args, **kwargs):
        """
        look | look around
        where | where am i | where is it

        """
        self.state = Operation.paused
        self.active.add(self.do_get)
        for i in self.world.visible.each:
            if i is not self.world.player:
                yield "* {0.names[0].noun}".format(i)

        yield from ("* {0}".format(i.label.title()) for i in self.world.player.location.options)

    def do_next(self, this, text, presenter, *args, **kwargs):
        """
        more | next

        """
        self.state = self.next_states(0)[1]

        if self.get_state(Journey) == Journey.ordeal:
            return next(self.flow)
        else:
            return random.choice([
                f"{self.world.player.name} hesitates.",
                f"{self.world.player.name} pauses.",
                f"{self.world.player.name} waits in the {self.world.player.location.title} for a moment.",
            ])

    def do_quit(self, this, text, presenter, *args, **kwargs):
        """
        quit

        """
        self.state = Operation.ending
