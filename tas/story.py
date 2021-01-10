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

from turberfield.catchphrase.drama import Drama
from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tas
from tas.sympathy import TeaAndSympathy

version = tas.__version__


class Story(Renderer):
    """
    Some methods of this class are likely to end up in a later
    version of the Catchphrase library.

    You should keep a regular eye on https://github.com/tundish/turberfield-catchphrase
    to spot new releases.

    """

    @staticmethod
    def build_presenter(folder, /, *args, ensemble=[], strict=True, roles=1):
        for n, p in enumerate(folder.paths):
            folder_dialogue = Drama.load_dialogue(folder.pkg, p)
            text = Drama.write_dialogue(folder_dialogue, *args)
            rv = Presenter.build_from_text(text, ensemble=ensemble, strict=strict, roles=roles, path=p)
            if rv:
                return (n, rv)
        else:
            return (None, None)

    def __init__(self, cfg=None, **kwargs):
        self.drama = TeaAndSympathy(**kwargs)
        self.definitions = {
            "catchphrase-colour-washout": "hsl(50, 0%, 100%, 1.0)",
            "catchphrase-colour-shadows": "hsl(202.86, 100%, 4.12%)",
            "catchphrase-colour-midtone": "hsl(203.39, 96.72%, 11.96%)",
            "catchphrase-colour-hilight": "hsl(203.06, 97.3%, 56.47%)",
            "catchphrase-colour-glamour": "hsl(353.33, 96.92%, 12.75%)",
            "catchphrase-colour-gravity": "hsl(293.33, 96.92%, 12.75%)",
        }
        self.settings = Settings(**self.definitions)

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    @property
    def dwell(self):
        return float(getattr(self.settings, "catchphrase-timing-dwell", "0.3"))

    @property
    def pause(self):
        return float(getattr(self.settings, "catchphrase-timing-pause", "1.0"))

    def represent(self, lines=[]):
        n, presenter = self.build_presenter(
            self.drama.folder, *lines,
            ensemble=self.drama.ensemble + [self.drama, self.settings]
        )
        return presenter


def parser():
    return argparse.ArgumentParser()


def main(args):
    story = Story(**vars(args))
    lines = []
    while story.drama.active:
        presenter = story.represent(lines)
        for frame in presenter.frames:
            animation = presenter.animate(frame, dwell=presenter.dwell, pause=presenter.pause)
            if not animation:
                continue
            for line, duration in story.render_frame_to_terminal(animation):
                print(line, "\n")
                time.sleep(duration)

        else:

            if story.drama.outcomes["finish"]:
                break

            cmd = input("{0} ".format(story.drama.prompt))
            fn, args, kwargs = story.drama.interpret(story.drama.match(cmd))
            lines = list(story.drama(fn, *args, **kwargs))

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
