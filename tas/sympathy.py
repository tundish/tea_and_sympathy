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
import itertools
import random

from turberfield.catchphrase.parser import CommandParser
from turberfield.dialogue.model import SceneScript

from tas.tea import execute
from tas.tea import promise
from tas.teatime import Motivation
from tas.teatime import Operation
from tas.teatime import Location
from tas.teatime import TeaTime
from tas.types import Character

from turberfield.catchphrase.mediator import Mediator
from turberfield.dialogue.types import Stateful



class MyDrama(Stateful, Mediator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = "?"
        self.input_text = ""
        self.default_fn = None

    @property
    def ensemble(self):
        raise NotImplementedError

    @property
    def turns(self):
        return len(self.history)

    def build(self):
        return []

    def play(self, cmd: str, casting:dict) -> dict:
        self.input_text = cmd
        fn, args, kwargs = self.interpret(self.match(cmd, context=casting, ensemble=self.ensemble))
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
    def fumble(self):
        # TODO: Make a setter to defeat a Tidy promise.
        return False

    def build(self):
        return [
            Character(names=["Sophie"]).set_state(Motivation.acting),
            Character(names=["Louise"]).set_state(Motivation.player),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = self.active.union(
            {self.do_again, self.do_look,
             self.do_help, self.do_history, self.do_quit}
        )
        self.default_fn = self.do_next

        self.lookup = defaultdict(set)
        for item in self.build():
            for n in item.names:
                self.lookup[n].add(item)

        self.p = promise()
        self.flow = execute(self.p, mugs=2, tea=2, milk=2, spoons=1, sugar=1)
        self.state = Operation.normal

    def do_again(self, this, text, casting, *args, **kwargs):
        """
        again | back

        """
        n = len(list(itertools.takewhile(
            lambda x: x.name == this.__name__, self.history
        )))
        self.state = max(0, self.state - (n + 1))
        return "again..."

    def do_next(self, this, text, casting, *args, **kwargs):
        """
        more | next

        """
        return next(self.flow)

    def do_look(self, this, text, casting, *args, **kwargs):
        """
        look | look around | look around kitchen
        search | search kitchen
        where | where am i | where is it

        """
        self.state = Operation.paused
        return "* kitchen"

    def do_help(self, this, text, casting, *args, **kwargs):
        """
        help

        """
        self.state = Operation.paused
        options = {fn.__name__: list(CommandParser.expand_commands(fn, self.ensemble)) for fn in self.active}
        yield from ("* {0[0][0]}".format(random.sample(v, 1)) for k, v in sorted(options.items()))

    def do_history(self, this, text, casting, *args, **kwargs):
        """
        history

        """
        self.state = Operation.paused
        yield from ("*{0.args[0]}*".format(i) for i in self.history if i.args[0])

    def do_quit(self, this, text, casting, *args, **kwargs):
        """
        quit

        """
        self.state = Operation.ending
