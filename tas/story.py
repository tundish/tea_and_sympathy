#!/usr/bin/env python3
#   encoding: utf-8

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

import argparse
import difflib
import enum
import functools
import re
import sys
import time
import operator

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.matcher import Matcher
from turberfield.dialogue.model import Model
from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful

# import logging
# logging.basicConfig(level=logging.DEBUG)

from tas.sympathy import TeaAndSympathy


class Story(Renderer):

    def __init__(self, cfg=None, **kwargs):
        # TODO: a heapq
        self.drama = TeaAndSympathy(**kwargs)
        self.definitions = {}
        story_section = {}
        self.settings = Settings(**dict(self.definitions, **story_section))


def parser():
    rv = argparse.ArgumentParser()
    rv.add_argument("--profanity", default=False, action="store_true", help="Permit adult language.") 
    return rv

def main(args):
    story = Story(**vars(args))
    while story.drama.active:
        text = input("? ")
        fn, args, kwargs = story.drama.interpret(story.drama.match(text))
        results = list(story.drama(fn, *args, **kwargs))
        rv = list(Presenter.build_shots(*results, shot="Epilogue"))
        n, presenter = Presenter.build_from_folder(
            *Presenter.build_shots(*results, shot="Epilogue"),
            folder=story.drama.folder,
            ensemble=story.drama.ensemble + [story.settings],
            strict=True
        )

        for frame in presenter.frames:
            animation = presenter.animate(frame)
            if not animation:
                continue
            for line, duration in story.render_frame_to_terminal(animation):
                print(line)
                time.sleep(duration)

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
