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
import sys
import time

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tas
from tas.sympathy import TeaAndSympathy

version = tas.__version__


class Story(Renderer):

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    def __init__(self, cfg=None, **kwargs):
        self.drama = TeaAndSympathy(**kwargs)
        self.definitions = {
            "catchphrase-colour-washout": "hsl(50, 0%, 100%, 1.0)",
            "catchphrase-colour-shadows": "hsl(37, 93%, 12%, 0.7)",
            "catchphrase-colour-midtone": "hsl(86, 93%, 12%, 0.7)",
            "catchphrase-colour-hilight": "hsl(224, 70%, 16%, 0.7)",
            "catchphrase-colour-glamour": "hsl(76, 80%, 35%, 1.0)",
            "catchphrase-colour-gravity": "hsl(36, 20%, 18%, 1.0)",
        }
        self.settings = Settings(**self.definitions)


def parser():
    return argparse.ArgumentParser()


def main(args):
    story = Story(**vars(args))
    results = []
    while story.drama.active and story.refresh_target("/") == "/":
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
        else:
            cmd = input("{0}: ".format(story.drama.prompt))
            fn, args, kwargs = story.drama.interpret(story.drama.match(cmd))
            results = list(story.drama(fn, *args, **kwargs))


def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
