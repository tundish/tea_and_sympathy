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


from collections import Counter
import enum
import random
import re
import statistics

from turberfield.catchphrase.drama import Drama
from turberfield.dialogue.types import Stateful

from tas.types import Feature
from tas.types import Item
from tas.types import Liquid
from tas.types import Mass
from tas.types import Named
from tas.types import Space


@enum.unique
class Motivation(enum.Enum):

    acting = 0
    paused = 1
    player = 2


class Location(enum.Enum):
    drawer = ["drawer"]
    fridge = ["fridge"]
    shelf = ["shelf"]
    sink = ["sink"]
    hob = ["hob", "cooker"]
    counter = ["counter"]

    @property
    def away(self):
        return {
            Location.drawer: ["out", "from out of"],
            Location.fridge: ["out", "from out of"],
            Location.sink: ["from out of"],
            Location.shelf: ["down from", "off"]
        }.get(self, ["from off", "off"])

    @property
    def into(self):
        return {
            Location.drawer: ["in"],
            Location.fridge: ["in"],
            Location.shelf: ["up on", "on"]
        }.get(self, ["on"])


class TeaTime(Drama):

    validator = re.compile("[\\w ]+")

    @staticmethod
    def build():
        rv = [
            Liquid(names=["milk"]).set_state(Location.fridge, 4),
            Liquid(names=["water", "tap"]).set_state(Location.sink, 20),
            Mass(names=["sugar"]).set_state(Location.shelf),
            Space(names=["kettle"]).set_state(Location.hob, 20),
            Feature(names=["hob"]).set_state(Location.hob, Motivation.paused),
            Space(names=["mug"], colour="red").set_state(Location.shelf, 10),
            Space(names=["mug"], colour="white").set_state(Location.shelf, 10),
            Space(names=["mug"], colour="yellow").set_state(Location.shelf, 10),
            Space(names=["bin", "rubbish", "trash"]).set_state(Location.sink),
        ]
        rv.extend([Space(names=["spoon"], n=n).set_state(Location.drawer) for n in range(2)])
        rv.extend([Item(names=["teabag", "tea"], n=n).set_state(Location.shelf, 20) for n in range(2)])
        return rv

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_look)
        self.active.add(self.do_search)
        self.active.add(self.do_examine)
        self.active.add(self.do_find)
        self.active.add(self.do_drop_item)
        self.active.add(self.do_pour_liquid)
        self.active.add(self.do_put_the_kettle_on)

    def __call__(self, fn, *args, **kwargs):
        kettle = next(iter(self.lookup["kettle"]))
        hob = next(iter(self.lookup["hob"]))
        if any("water" in i.names for i in kettle.contents(self.ensemble)):
            if kettle.get_state(Location) == Location.hob and hob.get_state(Motivation) == Motivation.acting:
                kettle.set_state(min(kettle.state + 10, 100))

        if kettle.state == 100:
            hob.state = Motivation.paused

        yield from super().__call__(fn, *args, **kwargs)

    def prioritise(self, match):
        """
        This method is a comparator for drama parser matches .
        It creates a score from the objects in the keyword arguments.
        It operates two measures:
            * location priority of the objects
            * their average temperature

        """
        fn, args, kwargs = match
        if not kwargs:
            return (0, 0)

        location_priorities = {i: n for n, i in enumerate(Location)}
        location_priority = statistics.mean(
            location_priorities[i] if isinstance(i, Location) else location_priorities[i.get_state(Location)]
            for i in kwargs.values()
        )
        try:
            return (
                location_priority,
                statistics.mean(
                    i.state for obj in kwargs.values()
                    for i in (obj.contents(self.ensemble) if hasattr(obj, "contents") else [])
                )
            )
        except statistics.StatisticsError:
            return (location_priority, statistics.mean(getattr(obj, "state", 0) for obj in kwargs.values()))

    def interpret(self, options):
        prioritised = sorted(options, key=self.prioritise, reverse=True)
        return prioritised[0]

    def do_look(self, this, text, *args):
        """
        look | look around | look around kitchen
        search | search kitchen
        poke about
        find
        where | where am i | where is it
        x

        """
        yield "You look around. You see:"
        yield from ("* the {0}".format(i.value[0].capitalize()) for i in list(Location))

    def do_examine(self, this, text, /, *, obj: [Item, Liquid, Mass, Space]):
        """
        examine {obj.names[0]} | check {obj.names[0]} | inspect {obj.names[0]} | search {obj.names[0]}
        examine {obj.names[1]} | check {obj.names[1]} | inspect {obj.names[1]} | search {obj.names[1]}

        """
        locn = obj.get_state(Location)
        adj = getattr(obj, "colour", "") or getattr(obj, "heat", "")
        yield f"The {adj} {obj.names[0]} is {locn.into[0]} the {locn.value[0]}."

        if isinstance(obj, Space):
            contents = obj.contents(self.ensemble)
            if contents:
                yield "It contains:"
                for i in contents:
                    adj = getattr(i, "colour", "") or getattr(i, "heat", "")
                    yield f"* {adj} {i.names[0]}"
            else:
                yield "It's empty."

    def do_search(self, this, text, /, *, locn: Location):
        """
        examine {locn.value[0]} | check {locn.value[0]} | inspect {locn.value[0]} | search {locn.value[0]}
        examine {locn.value[1]} | check {locn.value[1]} | inspect {locn.value[1]} | search {locn.value[1]}

        """
        items = [i for i in self.ensemble if isinstance(i, Stateful) and i.get_state(Location) == locn]
        counts = Counter(i.names[0] for i in items)
        yield "Looking {0.into[0]} the {0.value[0]}, you see:".format(locn)
        for i in items:
            if getattr(i, "parent", i) == i:
                yield "* {0}{1}".format(i.names[0].capitalize(), "s" if counts[i.names[0]] > 1 else "")

    def do_find(self, this, text, /, *, obj: [Item, Liquid, Mass, Space]):
        """
        find {obj.names[0]} | get {obj.names[0]} | grab {obj.names[0]} | pick up {obj.names[0]}
        find {obj.names[1]} | get {obj.names[1]} | grab {obj.names[1]} | pick up {obj.names[1]}

        get {obj.colour} {obj.names[0]} | get {obj.colour} {obj.names[1]}
        grab {obj.colour} {obj.names[0]} | grab {obj.colour} {obj.names[1]}
        find {obj.colour} {obj.names[0]} | find {obj.colour} {obj.names[1]}
        pick up {obj.colour} {obj.names[0]} | pick up {obj.colour} {obj.names[1]}

        """
        locn = obj.get_state(Location)

        colour = getattr(obj, "colour", "")
        yield f"You get the {colour} {obj.name} {locn.away[0]} the {locn.value[0]}."

        if "kettle" not in obj.names:
            obj.set_state(Location.counter)

        obj.state = max(20, obj.state)
        if isinstance(obj, Mass):
            self.active.add(self.do_pour_mass)

        locn = obj.get_state(Location)
        yield f"The {colour} {obj.name} is {locn.into[0]} the {locn.value[0]}."

    def do_pour_liquid(self, this, text, /, *, src: Liquid, dst: Space):
        """
        fill {dst.names[0]} with {src.heat} {src.names[0]} | fill {dst.names[0]} with {src.names[0]}
        fill {dst.names[0]} from {src.heat} {src.names[1]} | fill {dst.names[0]} from {src.names[1]}
        fill {dst.names[1]} with {src.heat} {src.names[0]} | fill {dst.names[1]} with {src.names[0]}
        fill {dst.names[1]} from {src.heat} {src.names[1]} | fill {dst.names[1]} from {src.names[1]}
        pour {src.names[0]} in {dst.names[0]} | pour {src.names[0]} into {dst.names[0]}
        pour {src.names[0]} in {dst.names[1]} | pour {src.names[0]} into {dst.names[1]}
        pour {src.names[1]} in {dst.names[0]} | pour {src.names[1]} into {dst.names[0]}
        pour {src.names[1]} in {dst.names[1]} | pour {src.names[1]} into {dst.names[1]}
        pour {src.heat} {src.names[0]} in {dst.names[0]} | pour {src.heat} {src.names[0]} into {dst.names[0]}
        pour {src.heat} {src.names[0]} in {dst.names[1]} | pour {src.heat} {src.names[0]} into {dst.names[1]}
        pour {src.heat} {src.names[1]} in {dst.names[0]} | pour {src.heat} {src.names[1]} into {dst.names[0]}
        pour {src.heat} {src.names[1]} in {dst.names[1]} | pour {src.heat} {src.names[1]} into {dst.names[1]}
        put {src.names[0]} in {dst.names[0]} | put {src.names[0]} into {dst.names[0]}
        put {src.names[0]} in {dst.names[1]} | put {src.names[0]} into {dst.names[1]}
        put {src.names[1]} in {dst.names[0]} | put {src.names[1]} into {dst.names[0]}
        put {src.names[1]} in {dst.names[1]} | put {src.names[1]} into {dst.names[1]}
        put {src.heat} {src.names[0]} in {dst.names[0]} | put {src.heat} {src.names[0]} into {dst.names[0]}
        put {src.heat} {src.names[0]} in {dst.names[1]} | put {src.heat} {src.names[0]} into {dst.names[1]}
        put {src.heat} {src.names[1]} in {dst.names[0]} | put {src.heat} {src.names[1]} into {dst.names[0]}
        put {src.heat} {src.names[1]} in {dst.names[1]} | put {src.heat} {src.names[1]} into {dst.names[1]}
        fill {dst.names[0]} | fill {dst.names[1]}
        add {src.names[0]} | add {src.names[1]}

        """
        kettle = next(iter(self.lookup["kettle"]))
        if "mug" in dst.names:
            if set(dst.contents(self.ensemble)).intersection(self.lookup["teabag"]) and kettle.state < 100:
                yield "To make tea, you need the water hotter."
                return

        if "water" in src.names and src.get_state(Location) == Location.sink:
            self.add(Liquid(names=["water", "tap"]).set_state(Location.sink, 20))

        heat = getattr(src, "heat", "")
        colour = getattr(dst, "colour", "")
        yield f"You pour the {heat} {src.names[0]} into the {colour} {dst.name}."

        dst.state = max(src.state, dst.state)
        src.state = dst.state
        src.parent = dst

        heat = getattr(src, "heat", "")
        if "kettle" in dst.names:
            self.active.add(self.do_heat_space)
        else:
            self.active.add(self.do_stir)
        yield f"The {src.names[0]} in the {colour} {dst.name} is {heat} ."

    def do_pour_mass(self, this, text, /, *, src: Mass, dst: Space):
        """
        pour {src.names[0]} in {dst.names[0]} | pour {src.names[0]} in {dst.names[0]}
        pour {src.names[0]} into {dst.names[1]} | pour {src.names[0]} into {dst.names[1]}
        put {src.names[0]} in {dst.names[0]} | put {src.names[0]} in {dst.names[0]}
        put {src.names[0]} into {dst.names[1]} | put {src.names[0]} into {dst.names[1]}

        """
        colour = getattr(dst, "colour", "")
        yield f"You pour the {src.names[0]} into the {colour} {dst.name}."
        src.parent = dst
        yield f"The {src.names[0]} is in the {colour} {dst.name}."

    def do_drop_item(self, this, text, /, *, src: Item, dst: Space):
        """
        drop {src.names[0]} in {dst.names[0]} | drop {src.names[0]} into {dst.names[0]}
        drop {src.names[1]} in {dst.names[0]} | drop {src.names[1]} into {dst.names[0]}
        put {src.names[0]} in {dst.names[0]}  | put {src.names[0]} into {dst.names[0]}
        put {src.names[1]} in {dst.names[0]}  | put {src.names[1]} into {dst.names[0]}

        """
        colour = getattr(dst, "colour", "")
        yield f"You drop the {src.names[0]} into the {colour} {dst.name}."
        src.parent = dst
        yield f"The {src.names[0]} is in the {colour} {dst.name}."

    def do_heat_space(self, this, text, /, *, obj: Space):
        """
        boil {obj.names[0]}
        heat {obj.names[0]}

        """
        obj.set_state(Location.hob)
        hob = next(iter(self.lookup["hob"]))
        hob.state = Motivation.acting
        kettle = next(iter(self.lookup["kettle"]))
        yield from self.do_examine(self.do_examine, text, obj=kettle)
        yield f"The water is at {obj.state}°."

    def do_stir(self, this, text, /, *, obj: [Item, Liquid]):
        """
        stir {obj.names[0]}
        stir {obj.names[1]}
        mash {obj.names[0]}
        mash {obj.names[1]}

        """
        mugs = {
            obj for obj in self.ensemble
            if "mug" in getattr(obj, "names", [])
            and obj.get_state(Location) == Location.counter
            and {"milk", "water"}.intersection(
                {n for i in obj.contents(self.ensemble) for n in getattr(i, "names", [])}
            )
        }
        spoons = {
            i for i in self.ensemble
            if "spoon" in getattr(i, "names", []) and i.get_state(Location) == Location.counter
        }
        if mugs and spoons:
            yield from (("You put a spoon in the {0.colour} mug and stir it.".format(mug) for mug in mugs))
        else:
            yield self.refusal

    def do_put_the_kettle_on(self, this, text, *args):
        """
        put the kettle on.

        """
        kettle = next(iter(self.lookup["kettle"]))
        tap = next(iter(self.lookup["tap"]))
        list(self.do_pour_liquid(self.do_pour_liquid, text, src=tap, dst=kettle))
        yield from self.do_heat_space(self.do_heat_space, text, obj=kettle)
        self.active.discard(this)
