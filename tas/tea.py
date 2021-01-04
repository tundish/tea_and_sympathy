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


from collections import defaultdict
from collections import Counter
import enum
import re
import statistics

from turberfield.catchphrase.drama import Drama
from turberfield.dialogue.types import Stateful

from tas.types import Named
from tas.types import Similar


@enum.unique
class Acting(enum.Enum):
    passive = 0
    active = 1


class Location(enum.Enum):
    DRAWER = ["drawer"]
    FRIDGE = ["fridge"]  # FIXME
    SHELF= ["shelf"]
    SINK = ["sink"]
    HOB = ["hob", "cooker"]
    COUNTER = ["counter"]


class Located(Stateful):

    @property
    def location(self):
        return self.get_state(Location)

class Liquid(Named, Similar):

    @property
    def heat(self):
        if self.state <= 20:
            return "cold"
        elif self.state >= 60:
            return "hot"
        else:
            return "warm"


class Feature(Named, Located): pass
class Item(Named, Similar): pass
class Mass(Named, Similar): pass


class Space(Named, Located):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = defaultdict(set)


class TeaTime(Drama):

    validator = re.compile("[\\w ]+")

    @staticmethod
    def prioritise(match):
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
                    i.state for obj in kwargs.values() for s in getattr(obj, "contents", {}).values() for i in s
                )
            )
        except statistics.StatisticsError:
            return (location_priority, statistics.mean(getattr(obj, "state", 0) for obj in kwargs.values()))

    @staticmethod
    def build():
        rv = [
            Liquid(names=["milk"]).set_state(Location.FRIDGE, 4),
            Liquid(names=["water", "tap"]).set_state(Location.SINK, 20),
            Mass(names=["sugar"]).set_state(Location.SHELF),
            Space(names=["kettle"]).set_state(Location.HOB, 20),
            Feature(names=["hob"]).set_state(Location.HOB, Acting.passive),
            Space(names=["mug"], colour="red").set_state(Location.SHELF, 10),
            Space(names=["mug"], colour="white").set_state(Location.SHELF, 10),
            Space(names=["mug"], colour="yellow").set_state(Location.SHELF, 10),
            Space(names=["bin", "rubbish", "trash"]).set_state(Location.SINK),
        ]
        rv.extend([Space(names=["spoon"], n=n).set_state(Location.DRAWER) for n in range(2)])
        rv.extend([Item(names=["teabag", "tea"], n=n).set_state(Location.SHELF, 20) for n in range(2)])
        return rv

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_examine)
        self.active.add(self.do_find)
        self.active.add(self.do_look)
        self.active.add(self.do_drop_item)
        self.active.add(self.do_pour_liquid)
        self.active.add(self.do_put_the_kettle_on)
        self.outcomes = defaultdict(bool)

    def __call__(self, fn, *args, **kwargs):
        kettle = next(iter(self.lookup["kettle"]))
        hob = next(iter(self.lookup["hob"]))
        if kettle.contents["water"] and hob.get_state(Acting) == Acting.active:
            if kettle.get_state(Location) == Location.HOB:
                kettle.set_state(min(kettle.state + 10, 100))
                for s in kettle.contents.values():
                    for obj in s:
                        obj.state = kettle.state
        if kettle.state == 100:
            hob.state = Acting.passive

        yield from super().__call__(fn, *args, **kwargs)

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
        items = "\n".join("* the {0}".format(i.value[0].capitalize()) for i in list(Location))
        yield f"""You look around. You see:\n\n{items}\n"""

    def do_examine(self, this, text, /, *, locn: Location):
        """
        examine {locn.value[0]} | check {locn.value[0]} | inspect {locn.value[0]} | search {locn.value[0]}
        examine {locn.value[1]} | check {locn.value[1]} | inspect {locn.value[1]} | search {locn.value[1]}

        """
        counts = Counter(
            i.names[0]
            for i in self.ensemble
            if isinstance(i, Stateful)
            and i.get_state(Location) == locn
        )
        terms = ["* {0}{1}".format(k.capitalize(), "s" if v > 1 else "") for k, v in counts.items()]
        if "kettle" in terms and self.do_heat_space in self.active:
            kettle = next(i for i in self.ensemble if "kettle" in getattr(i, "names", []))
            yield from self.do_heat_space(self.do_heat_space, text, kettle)
        else:
            location = locn.value[0]
            at_the = {
                Location.DRAWER: "in the", Location.FRIDGE: "in the", Location.SHELF: "up on the"
            }.get(locn, "at the")
            yield "Looking {0} {1}, you see:\n".format(at_the, location)
            yield from terms

    def do_find(self, this, text, /, *, obj: [Item, Liquid, Mass, Space]):
        """
        find {obj.names[0]} | get {obj.names[0]} | grab {obj.names[0]} | pick up {obj.names[0]}
        find {obj.names[1]} | get {obj.names[1]} | grab {obj.names[1]} | pick up {obj.names[1]}

        get {obj.colour} {obj.names[0]} | get {obj.colour} {obj.names[1]}
        grab {obj.colour} {obj.names[0]} | grab {obj.colour} {obj.names[1]}
        find {obj.colour} {obj.names[0]} | find {obj.colour} {obj.names[1]}
        pick up {obj.colour} {obj.names[0]} | pick up {obj.colour} {obj.names[1]}

        """
        found_in = obj.get_state(Location)
        found_in_name = found_in.value[0]
        moved_to = Location.COUNTER
        from_the = "from out of the" if found_in in (
            Location.DRAWER, Location.FRIDGE, Location.SINK
        ) else "from off the"

        colour = getattr(obj, "colour", "")
        yield f"You get the {colour} {obj.name} {from_the} {found_in_name}."

        obj.set_state(Location.COUNTER)
        obj.state = max(20, obj.state)
        if isinstance(obj, Mass):
            self.active.add(self.do_pour_mass)

        yield f"The {colour} {obj.name} is on the {moved_to.value[0]}."

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
            if dst.contents["teabag"] and kettle.state < 100:
                yield "That's not how to make tea."
                return

        if "water" in src.names and src.get_state(Location) == Location.SINK:
            self.add(Liquid(names=["water", "tap"]).set_state(Location.SINK, 20))

        heat = getattr(src, "heat", "")
        colour = getattr(dst, "colour", "")
        yield f"You pour the {heat} {src.names[0]} into the {colour} {dst.name}."

        dst.contents[src.names[0]].add(src)
        src.state = dst.get_state(Location)
        dst.state = max(src.state, dst.state)
        for s in dst.contents.values():
            for obj in s:
                obj.state = max(obj.state, dst.state)

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
        dst.contents[src.names[0]].add(src)
        src.state = dst.get_state(Location)
        dst.state = max(src.state, dst.state)

        colour = getattr(dst, "colour", "")
        yield f"You pour the {src.names[0]} into the {colour} {dst.name}."
        yield f"The {src.names[0]} is in the {colour} {dst.name}."

    def do_drop_item(self, this, text, /, *, src: Item, dst: Space):
        """
        drop {src.names[0]} in {dst.names[0]} | drop {src.names[0]} into {dst.names[0]}
        drop {src.names[1]} in {dst.names[0]} | drop {src.names[1]} into {dst.names[0]}
        put {src.names[0]} in {dst.names[0]}  | put {src.names[0]} into {dst.names[0]}
        put {src.names[1]} in {dst.names[0]}  | put {src.names[1]} into {dst.names[0]}

        """
        colour = getattr(dst, "colour", "")
        if "mug" in dst.names:
            dst.state == Location.COUNTER
            if dst.contents[src.names[0]]:
                yield f"There's enough {src.names[0]}s in the {colour} {dst.names[0]} already."
                return

        yield f"You drop the {src.names[0]} into the {colour} {dst.name}."
        dst.contents[src.names[0]].add(src)
        src.state = dst.get_state(Location)
        src.state = max(src.state, dst.state)
        yield f"The {src.names[0]} is in the {colour} {dst.name}."

    def do_heat_space(self, this, text, /, *, obj: Space):
        """
        boil {obj.names[0]}
        check {obj.names[0]}
        heat {obj.names[0]}

        """
        obj.set_state(Location.HOB)
        hob = next(iter(self.lookup["hob"]))
        hob.state = Acting.active
        yield f"The {obj.name} is on the hob."
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
            and obj.get_state(Location) == Location.COUNTER
            and (obj.contents["milk"] or obj.contents["water"])
        }
        spoons = {
            i for i in self.ensemble
            if "spoon" in getattr(i, "names", []) and i.get_state(Location) == Location.COUNTER
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
