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

from collections import ChainMap
from collections import Counter
from collections import defaultdict
from collections import namedtuple
import enum
import functools
import logging
import random
import sys
import uuid

from proclets.channel import Channel
from proclets.proclet import Proclet
from proclets.types import Init
from proclets.types import Exit
from proclets.types import Termination


class Attribution(dict):

    def __init__(self, *args, uid=None, ts=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = uid
        self.ts = ts


class Fruition(enum.Enum):
    """
    Terry Winograd, Fernando Flores, Craig Larman

    """
    inception = 1
    elaboration = 2
    construction = 3
    transition = 4
    completion = 5
    discussion = 6
    defaulted = 7
    withdrawn = 8
    cancelled = 9

    def trigger(self, event=None):
        if self.value == 1:
            return {
                Init.request: Fruition.elaboration
            }.get(event, self)
        elif self.value == 2:
            return {
                Init.promise: Fruition.construction,
                Init.counter: Fruition.discussion,
                Init.abandon: Fruition.withdrawn,
                Init.decline: Fruition.withdrawn,
            }.get(event, self)
        elif self.value == 3:
            return {
                Exit.abandon: Fruition.cancelled,
                Exit.deliver: Fruition.transition,
                Exit.decline: Fruition.defaulted,
            }.get(event, self)
        elif self.value == 4:
            return {
                Exit.abandon: Fruition.cancelled,
                Exit.decline: Fruition.construction,
                Exit.confirm: Fruition.completion,
            }.get(event, self)
        elif self.value == 6:
            return {
                Init.promise: Fruition.construction,
                Init.confirm: Fruition.construction,
                Init.counter: Fruition.elaboration,
                Init.abandon: Fruition.withdrawn,
                Init.decline: Fruition.withdrawn,
            }.get(event, self)
        else:
            return self


class Promise(Proclet):

    Discourse = namedtuple("Discourse", ["uid", "channel", "reference", "fruition"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(self.name)
        self.actions = {}
        self.contents = {}
        self.discourse = defaultdict(dict) # FIXME
        self.fruition = defaultdict(functools.partial(Fruition, 1))
        self.intent = None

    @property
    def result(self):
        mappings = [
            next(
                (Attribution(m.content, ts=m.ts, uid=m.sender) for m in reversed(v) if m.action == Exit.deliver),
                Attribution()
            )
            for c in self.channels.values()
            for v in c.view(self.uid)
        ]
        return ChainMap(*reversed(list(filter(None, mappings))))

    def _fruition(self, k):
        speech = {}
        for d in list(self.discourse.get(k, {}).values()):
            if d.uid not in speech:
                speech.update(
                    {v[0].connect: v for v in self.channels[d.channel].view(self.uid)}  # FIXME view -> dict
                )

            state = Fruition.inception
            for m in speech[d.uid]:
                state = state.trigger(m.action)
            rv = self.discourse[k][d.uid] = self.discourse[k][d.uid]._replace(fruition=state)
            yield rv

    @property
    def pending(self):
        return [
            v
            for c in self.channels.values()
            for v in c.view(self.uid)
            if not any(i for i in reversed(v) if isinstance(i.action, Exit))
        ]

    @property
    def effort(self):
        return Counter(k for m in self.result.maps for k in m)

    def lacks(self, key, *classes: Proclet):
        return not (
            any(key in m.content
            for l in self.pending
            for m in l
            if any(isinstance(self.population.get(u), classes) for u in m.group)) or
            any(key in a for a in self.result.maps if isinstance(self.population.get(a.uid), classes))
        )

    def action(self, this, channel="public", **kwargs):
        return list(
            self.channels[channel].respond(
                self, this,
                actions=self.actions,
                contents=self.contents,
            )
        )


class Brew(Promise):

    @property
    def net(self):
        return {
            self.pro_filling: [self.pro_boiling, self.pro_missing],
            self.pro_missing: [self.pro_claiming],
            self.pro_boiling: [self.pro_brewing],
            self.pro_claiming: [self.pro_inspecting, self.pro_claiming],
            self.pro_inspecting: [self.pro_approving],
            self.pro_approving: [self.pro_brewing],
            self.pro_brewing: [self.pro_serving],
            self.pro_serving: [],
        }

    def pro_filling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        self.kettle = 20
        yield

    def pro_missing(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        print(*self.fruition.items(), sep="\n")
        if not any(
            self.fruition[k] in (Fruition.inception, Fruition.elaboration, Fruition.discussion)
            for k in kwargs
        ):
            yield

        for k, v in kwargs.items():
            if self.fruition[k] == Fruition.inception:
                p = Kit.create(
                    name=f"find_{k}",
                    channels=self.channels,
                    group=[self.uid],
                )
                yield p

                m = next(self.channels["public"].send(
                    sender=self.uid, group=[p.uid],
                    action=Init.request, content={k: v}
                ))
                self.fruition[k] = self.fruition[k].trigger(m.action)
                yield m

            if self.fruition[k] in (Fruition.elaboration, Fruition.discussion):
                for m in self.channels["public"].respond(self, this, actions=self.actions):
                    try:
                        self.fruition[k] = self.fruition[k].trigger(m.action)
                    except TypeError:
                        print(k, m)
                        raise

    def pro_boiling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        while self.kettle <= 90:
            self.kettle += 10
            return
        yield

    def pro_claiming(self, this, **kwargs):
        try:
            sync = next(
                i for i in self.channels["public"].receive(self, this)
                if i.action == Exit.deliver
            )
        except StopIteration:
            return
        else:
            self.log.info(self.result, extra={"proclet": self})
            yield

    def pro_inspecting(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        for k in ("mugs", "spoons"):
            if not self.lacks(k, Tidy):
                continue

            p = Tidy.create(
                name=f"clean_{k}",
                channels=self.channels,
                group=[self.uid],
            )
            yield p

            luck = kwargs.get("luck", random.triangular(0, 1, 3/4))
            yield from self.channels["public"].send(
                sender=self.uid, group=[p.uid],
                action=Init.request,
                content={k: kwargs[k], "luck": luck}
            )

        yield

    def pro_approving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        while self.pending:
            try:
                sync = next(
                    i for i in self.channels["public"].receive(self, this)
                    if isinstance(i.action, Exit)
                )
            except StopIteration:
                return
        else:
            self.log.info(self.result, extra={"proclet": self})
            yield

    def pro_brewing(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_serving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        if not self.pending:
            raise Termination()
            yield


class Kit(Promise):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = {
            Init.request: Init.promise,
        }

    @property
    def net(self):
        return {
            self.pro_missing: [self.pro_finding],
            self.pro_finding: [self.pro_claiming],
            self.pro_claiming: [],
        }

    def pro_missing(self, this, **kwargs):
        try:
            msgs = list(self.channels["public"].respond(self, this, actions=self.actions))
            self.intent = msgs[0]
        except IndexError:
            return
        else:
            self.log.info(self.intent, extra={"proclet": self})
        yield

    def pro_finding(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        for k, v in self.intent.content.items():
            self.log.info(f"Finding {k}", extra={"proclet": self})
        yield

    def pro_claiming(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield self.channels["public"].reply(
            self, self.intent, action=Exit.deliver, content=self.intent.content
        )
        yield


class Tidy(Promise):

    @property
    def net(self):
        return {
            self.pro_inspecting: [self.pro_cleaning],
            self.pro_cleaning: [self.pro_approving],
            self.pro_approving: [],
        }

    def pro_inspecting(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        try:
            self.intent = next(
                i for i in self.channels["public"].receive(self, this)
                if i.action == Init.request
            )
            self.luck = self.intent.content.pop("luck", 1)
        except StopIteration:
            return
        else:
            self.log.info(self.intent, extra={"proclet": self})
            yield
        yield

    def pro_cleaning(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        for k, v in self.intent.content.items():
            if random.random() > self.luck:
                self.log.info(f"Cleaning {k}", extra={"proclet": self})
        yield

    def pro_approving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield self.channels["public"].reply(
            self, self.intent, action=Exit.deliver, content=self.intent.content
        )
        yield


def promise_tea(**kwargs):
    name = kwargs.pop("name", "brew_tea")
    channels = {"public": Channel()}
    return Brew.create(name=name, channels=channels, **kwargs)

if __name__ == "__main__":
    logging.basicConfig(
        style="{", format="{proclet.name:>16}|{funcName:>14}|{message}",
        level=logging.INFO,
    )
    b = promise_tea()
    rv = None
    n = 0
    while rv is None:
        try:
            for m in b(mugs=2, tea=2, milk=2, spoons=1, sugar=1):
                logging.debug(m, extra={"proclet": b})
        except Termination:
            rv = 0
        except Exception as e:
            rv = 1
            logging.exception(e, extra={"proclet": b})
        finally:
            n += 1
            if n > 30:
                break

    sys.exit(rv)
