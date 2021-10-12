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
import textwrap

from turberfield.catchphrase.parser import CommandParser
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript

from tas.tea import execute
from tas.tea import promise
from tas.types import Article
from tas.types import Availability
from tas.types import Character
from tas.types import Consumption
from tas.types import Container
from tas.types import Journey
from tas.types import Location
from tas.types import Motivation
from tas.types import Name
from tas.types import Operation
from tas.types import Pronoun

from turberfield.catchphrase.mediator import Mediator
from turberfield.dialogue.types import Stateful


class MyDrama(Stateful, Mediator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = "?"
        self.input_text = ""
        self.default_fn = None
        self.valid_states = [0]

    @property
    def ensemble(self):
        raise NotImplementedError

    @property
    def turns(self):
        return len(self.history)

    def __call__(self, fn, *args, **kwargs):
        text, presenter, *_ = args
        if presenter and (presenter.dwell or presenter.pause):
            self.valid_states = self.find_valid_states(presenter)

        return super().__call__(fn, *args, **kwargs)

    def build(self):
        return []

    def find_valid_states(self, presenter):
        return sorted(
            c.value for f in presenter.frames for c in f[Model.Condition]
            if c.object is self and c.format == "state" and isinstance(c.value, int)
        ) or [0]

    def next_states(self, n=1):
        fwd = min(bisect.bisect_right(self.valid_states, self.state) + n - 1, len(self.valid_states) - 1)
        bck = max(0, bisect.bisect_left(self.valid_states, self.state) - n)
        rv = (self.valid_states[bck], self.valid_states[fwd])
        return rv

    def deliver(self, cmd, presenter):
        self.input_text = cmd
        fn, args, kwargs = self.interpret(self.match(cmd, context=presenter, ensemble=self.ensemble))
        fn = fn or self.default_fn
        return fn and self(fn, *args, **kwargs)


class Sympathy(MyDrama):

    @property
    def ensemble(self):
        return list({i for s in self.lookup.values() for i in s})

    @property
    def folder(self):
        return SceneScript.Folder(
            pkg="tas.dlg",
            description="Tea and Sympathy",
            metadata={},
            paths=[
                "enter.rst", # "explore.rst", "funnel.rst",
                "pause.rst", "quit.rst"
                # "verdict"
            ],
            interludes=None
        )

    @property
    def local(self):
        reach = (self.player.location, Location.inventory)
        return [i for i in self.ensemble if i.get_state(Location) in reach]

    @functools.cached_property
    def player(self):
        return next(i for i in self.ensemble if i.get_state(Motivation) == Motivation.player)

    @property
    def fumble(self):
        # TODO: Make a setter to defeat a Tidy promise.
        return False

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
                contents=Consumption.cigarette
            ).set_state(Location.bedroom, Availability.removed),
            Character(
                names=[Name("Sophie", Article("", ""), Pronoun("she", "her", "herself", "hers"))],
                description="{0.name} goes to art college."
            ).set_state(Motivation.acting, Location.kitchen),
            Character(
                names=[Name("Louise", Article("", ""), Pronoun("she", "her", "herself", "hers"))],
                description="{0.name} is a young woman from Manchester. She works as a nurse."
            ).set_state(Motivation.player, Location.bedroom),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = self.active.union(
            {self.do_again, self.do_look,
             self.do_go, self.do_inspect,
             self.do_help, self.do_history, self.do_quit}
        )
        self.default_fn = self.do_next

        self.lookup = defaultdict(set)
        for item in self.build():
            for n in item.names:
                self.lookup[n].add(item)

        self.p = promise()
        self.flow = execute(self.p, mugs=2, tea=2, milk=2, spoons=1, sugar=1)
        self.set_state(Journey.mentor)
        self.set_state(Operation.normal)

    def do_again(self, this, text, presenter, *args, **kwargs):
        """
        again | back

        """
        n = len(list(itertools.takewhile(
            lambda x: x.name == this.__name__, self.history
        ))) + 1
        self.state = self.next_states(n)[0]
        return "again..."

    def do_consume(self, this, text, presenter, obj: "local", *args, **kwargs):
        """
        {obj.contents.value.verb.imperative} {obj.contents.value.name.noun}

        """
        self.player.state = obj.contents
        return obj.description.format(obj, **self.facts)

    def do_get(self, this, text, presenter, obj: Container, *args, **kwargs):
        """
        get {obj.names[0].noun}
        grab {obj.names[0].noun}
        take {obj.names[0].noun}
        pick up {obj.names[0].noun}

        """
        obj.state = Location.inventory
        self.active.discard(this)
        return f"{self.player.name} picks up {obj.names[0].article.definite} {obj.names[0].noun}.",

    def do_go(self, this, text, presenter, *args, locn: "player.location.options", **kwargs):
        """
        enter {locn.value[0]} | enter {locn.value[1]}
        go {locn.value[0]} | go {locn.value[1]} | go {locn.value[2]} | go {locn.value[3]} | go {locn.value[4]}

        """
        if self.player.get_state(Location) == locn:
            yield random.choice([
                f"{self.player.name} stays in the {locn.title}.",
                f"{self.player.name} is already in the {locn.title}.",
                f"{self.player.name} decides to remain in the {locn.title}."
            ])
        elif locn == Location.stairs:
            yield f"{self.player.name} looks upward."
            yield "The stairs lead to an attic gallery, and Sophie's room."
            yield f"{self.player.name} hesitates."
            yield "She doesn't want to go up there."
        else:
            self.state = 0
            self.player.state = locn
            yield f"{self.player.name} goes into the {locn.title}."

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
                if not any(
                    isinstance(i, Stateful) and i.get_state(Availability) == Availability.removed
                    for i in kwargs.values()
                ):
                    cmds.append(cmd)

            if cmds:
                yield "* {0}".format(random.choice(cmds))

    def do_history(self, this, text, presenter, *args, **kwargs):
        """
        history

        """
        self.state = Operation.paused
        yield from ("* {0.args[0]}".format(i) for i in self.history if i.args[0])

    def do_inspect(self, this, text, presenter, obj: "local", *args, **kwargs):
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
        for i in self.local:
            if i is not self.player:
                yield "* {0.names[0].noun}".format(i)

            if isinstance(i, Container):
                self.active.add(self.do_get)

        yield from ("* {0}".format(i.label.title()) for i in self.player.location.options)

    def do_next(self, this, text, presenter, *args, **kwargs):
        """
        more | next

        """
        self.state = self.next_states(0)[1]

        if self.get_state(Journey) == Journey.ordeal:
            return next(self.flow)
        else:
            return random.choice([
                f"{self.player.name} hesitates.",
                f"{self.player.name} waits.",
            ])

    def do_quit(self, this, text, presenter, *args, **kwargs):
        """
        quit

        """
        self.state = Operation.ending
