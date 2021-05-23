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
import textwrap

from turberfield.dialogue.model import SceneScript

from tas.tea import Motivation
from tas.tea import Location
from tas.tea import TeaTime
from tas.types import Character


class TeaAndSympathy(TeaTime):

    @property
    def folder(self):
        return SceneScript.Folder(
            pkg="tas.dlg",
            description="Tea and Sympathy",
            metadata={},
            paths=["early.rst", "kettle.rst", "made.rst", "pause.rst", "quit.rst"],
            interludes=None
        )

    def build(self):
        yield from super().build()
        yield from [
            Character(names=["Sophie"]).set_state(Motivation.acting),
            Character(names=["Louise"]).set_state(Motivation.player),
        ]

    def pause(self, *args):
        args = args or [Motivation.acting]
        for i in self.ensemble:
            if isinstance(i, Character) and i.get_state(Motivation) in args:
                i.state = Motivation.paused

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = defaultdict(bool)
        self.active.add(self.do_history)
        self.active.add(self.do_quit)
        self.refusal = "That's not an option right now."
        self.input_text = ""
        self.prompt = "?"

    def __call__(self, fn, *args, **kwargs):
        try:
            rv = super().__call__(fn, *args, **kwargs)
        except TypeError:
            rv = self.do_refuse(self.do_refuse, self.input_text, **kwargs)

        try:
            mugs = [i for i in self.lookup["mug"] if i.get_state(Location) == Location.counter]
            contents = [i.contents(self.ensemble) for i in mugs]
            self.outcomes["brewed"] = self.outcomes["brewed"] or any(i for i in self.lookup["tea"] if i.state == 100)
            self.outcomes["untidy"] = any(i for c in contents for i in c if "tea" in getattr(i, "names", []))
            self.outcomes["stingy"] = not any(i for c in contents for i in c if "milk" in getattr(i, "names", []))
            self.outcomes["sugary"] = any(i for c in contents for i in c if "sugar" in getattr(i, "names", []))
            self.outcomes["served"] = (
                self.outcomes["brewed"] and not self.outcomes["untidy"] and not self.outcomes["stingy"]
            )
            self.outcomes["finish"] = all(
                i.get_state(Motivation) == Motivation.paused
                for i in self.ensemble if isinstance(i, Character)
            )
            self.outcomes["paused"] = (
                any(i.get_state(Motivation) == Motivation.paused
                for i in self.ensemble if isinstance(i, Character))
                and not self.outcomes["finish"]
            )
        except StopIteration:
            pass
        finally:
            return rv

    def do_history(self, this, text, /, **kwargs):
        """
        history

        """
        self.pause()
        return textwrap.dedent("""
        [MEDIATOR]_
        So far, it's been like this.
        """) + "\n".join(
            ("*{0.args[0]}*".format(i) for i in self.history)
        )

    def do_refuse(self, this, text, /, **kwargs):
        """
        refuse

        """
        # FIXME: This doeasn't work.
        self.prompt = "If you're stuck, try 'help' or 'history'."
        self.pause()

        return "\n".join(("[MEDIATOR]_", text, self.refusal))

    def do_quit(self, this, text, /, **kwargs):
        """
        exit | finish | stop | quit

        """
        self.pause(Motivation.acting, Motivation.player)
