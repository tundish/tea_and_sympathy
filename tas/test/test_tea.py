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

import unittest

from collections import ChainMap
from collections import Counter
import logging
import sys
from types import SimpleNamespace
import uuid

from proclets.channel import Channel
from proclets.proclet import Proclet
from proclets.types import Init
from proclets.types import Exit
from proclets.types import Termination



class Construct(ChainMap):

    @classmethod
    def create(cls, uid=None, **kwargs):
        uid = uid or uuid.uuid4()
        return cls(uid, Counter(**kwargs))

    def __init__(self, uid, *maps):
        super().__init__(*maps)
        self.uid = uid

class Promise(Proclet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(self.name)
        self.intent = {}
        self.result = {}


class Brew(Promise):

    @property
    def net(self):
        return {
            self.pro_filling: [self.pro_boiling, self.pro_missing],
            self.pro_missing: [self.pro_claiming], # self.pro_missing],
            self.pro_boiling: [self.pro_brewing],
            self.pro_claiming: [self.pro_inspecting, self.pro_claiming],
            self.pro_inspecting: [self.pro_approving],
            self.pro_approving: [self.pro_brewing],
            self.pro_brewing: [self.pro_serving],
            self.pro_serving: [],
        }

    def pro_filling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_missing(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        self.intent.update(kwargs)
        for k, v in kwargs.items():
            if not self.result.get(k):
                p = Kit.create(
                    name=f"find_{k}",
                    channels=self.channels,
                    group=[self.uid],
                )
                yield p
                yield from self.channels["public"].send(
                    sender=self.uid, group=[p.uid],
                    action=this.__name__, content={k: v}
                )
        yield

    def pro_boiling(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_claiming(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_inspecting(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_approving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_brewing(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_serving(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        raise Termination()
        yield


class Kit(Promise):

    @property
    def net(self):
        return {
            self.pro_missing: [self.pro_finding],
            self.pro_finding: [self.pro_claiming],
            self.pro_claiming: [],
        }

    def pro_missing(self, this, **kwargs):
        try:
            sync = next(
                i for i in self.channels["public"].receive(self, this)
                if i.action == this.__name__
            )
            self.log.debug(sync, extra={"proclet": self})
        except StopIteration:
            return
        else:
            self.log.info(sync, extra={"proclet": self})
            yield
        yield

    def pro_finding(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
        yield

    def pro_claiming(self, this, **kwargs):
        self.log.info("", extra={"proclet": self})
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
        yield

    def pro_cleaning(self, this, **kwargs):
        yield

    def pro_approving(self, this, **kwargs):
        yield


class TypeTests(unittest.TestCase):

    def test_construct(self):
        c = Construct.create()
        self.assertIsInstance(c.uid, uuid.UUID)

if __name__ == "__main__":
    logging.basicConfig(
        style="{", format="{proclet.name:>16}|{funcName:>14}|{message}",
        level=logging.INFO,
    )
    channels = {"public": Channel()}
    b = Brew.create(name="brew_tea", channels=channels)
    rv = None
    while rv is None:
        try:
            for m in b(tea=2, milk=2, sugar=1):
                logging.debug(m, extra={"proclet": b})
        except Termination:
            rv = 0
        except Exception as e:
            rv = 1
            logging.exception(e, extra={"proclet": b})

    sys.exit(rv)
