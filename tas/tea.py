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
from collections import deque
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

from tas.promise import Fruition
from tas.promise import Promise


class Brew(Promise):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = {
            Exit.deliver: Exit.confirm,
        }

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
        jobs = [tuple({k: v}.items()) for k, v in kwargs.items()]
        if all(self.fruition[j] == Fruition.construction for j in jobs):
            yield

        for j in jobs:
            if self.fruition[j] == Fruition.inception:
                p = Kit.create(
                    name=f"find_{j[0][0]}",
                    channels=self.channels,
                    group=[self.uid],
                )
                yield p

                m = next(self.channels["public"].send(
                    sender=self.uid, group=[p.uid],
                    action=Init.request, content=dict(j)))
                self.fruition[j] = self.fruition[j].trigger(m.action)
                yield m

        for m in self.channels["public"].respond(self, this, actions=self.actions):
            try:
                j = tuple(m.content.items())
                self.fruition[j] = self.fruition[j].trigger(m.action)
            except AttributeError:
                self.log.debug(m, extra={"proclet": self})
            finally:
                yield m

    def pro_boiling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        while self.kettle <= 90:
            self.kettle += 10
            return
        yield

    def pro_claiming(self, this, **kwargs):
        for m in self.channels["public"].respond(
            self, this, actions=self.actions, contents=self.contents
        ):
            self.contents[m.action] = m.content
            try:
                j = tuple(m.content.items())
                self.fruition[j] = self.fruition[j].trigger(m.action)
            except AttributeError:
                return
            else:
                self.log.info(self.fruition, extra={"proclet": self})
                yield

    def pro_inspecting(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        jobs = [tuple({k: v}.items()) for k, v in kwargs.items() if k in ("mugs", "spoons")]
        if all(
            self.dispatched(j, Tidy) and self.fruition[j] == Fruition.construction for j in jobs
        ):
            yield

        for j in jobs:
            if self.dispatched(j, Tidy):
                continue

            self.fruition[j] = Fruition.inception
            p = Tidy.create(
                name=f"clean_{j[0][0]}",
                channels=self.channels,
                group=[self.uid],
            )
            yield p

            luck = kwargs.get("luck", random.triangular(0, 1, 3/4))
            luck = 1
            m = next(self.channels["public"].send(
                sender=self.uid, group=[p.uid],
                action=Init.request, content=dict(j)
            ))
            self.fruition[j] = self.fruition[j].trigger(m.action)
            yield m

        for m in self.channels["public"].respond(self, this, actions=self.actions, contents=self.contents):
            try:
                j = tuple(m.content.items())
                self.fruition[j] = self.fruition[j].trigger(m.action)
            except AttributeError:
                self.log.debug(m, extra={"proclet": self})
            finally:
                yield m

    def pro_approving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        while any(i for i in self.fruition.values() if i != Fruition.completion):
            self.log.info(self.fruition, extra={"proclet": self})
            for m in self.channels["public"].respond(
                self, this, actions=self.actions, contents=self.contents
            ):
                self.contents[m.action] = m.content
                try:
                    j = tuple(m.content.items())
                    self.fruition[j] = self.fruition[j].trigger(m.action)
                except AttributeError:
                    return
        else:
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
            self.pro_init: [self.pro_finding],
            self.pro_finding: [self.pro_exit],
            self.pro_exit: [],
        }

    def pro_finding(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        for job in self.fruition:
            for k in dict(job):
                self.log.info(f"Finding {k}", extra={"proclet": self})
        yield


class Tidy(Promise):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = {
            Init.request: Init.promise,
        }

    @property
    def net(self):
        return {
            self.pro_init: [self.pro_cleaning],
            self.pro_cleaning: [self.pro_exit],
            self.pro_exit: [],
        }

    def pro_init(self, this, **kwargs):
        for n, m in enumerate(
            self.channels["public"].respond(self, this, actions=self.actions, contents=self.contents)
        ):
            self.luck = m.content.pop("luck", 1)
            self.contents[m.action] = m.content
            job = tuple(self.contents[Init.request].items())
            self.fruition[job] = self.fruition[job].trigger(m.action)

            if not n:
                self.requests[job].append(m)

        if all(i == Fruition.construction for i in self.fruition.values()):
            self.log.info(self.requests, extra={"proclet": self})
            yield

    def pro_cleaning(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        for k in self.fruition:
            if random.random() > self.luck:
                self.log.info(f"Cleaning {k}", extra={"proclet": self})
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
                logging.info(m, extra={"proclet": b})
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
