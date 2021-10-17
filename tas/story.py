#!/usr/bin/env python3
#   encoding: utf-8

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

import argparse
import sys
import time

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Action
from turberfield.catchphrase.render import Parameter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tas
from tas.sympathy import Sympathy
from tas.types import Operation

version = tas.__version__


class Story(Renderer):
    """
    Some methods of this class are likely to end up in a later
    version of the Catchphrase library.

    You should keep a regular eye on https://github.com/tundish/turberfield-catchphrase
    to spot new releases.

    """

    def __init__(self, cfg=None, **kwargs):
        self.drama = {
            "sympathy": Sympathy(**kwargs)
        }
        self.context = self.drama["sympathy"]
        self.definitions = {
            "catchphrase-colour-washout": "hsl(50, 0%, 100%, 1.0)",
            "catchphrase-colour-shadows": "hsl(202.86, 100%, 4.12%)",
            "catchphrase-colour-midtone": "hsl(203.39, 96.72%, 11.96%)",
            "catchphrase-colour-hilight": "hsl(203.06, 97.3%, 56.47%)",
            "catchphrase-colour-glamour": "hsl(353.33, 96.92%, 12.75%)",
            "catchphrase-colour-gravity": "hsl(293.33, 96.92%, 12.75%)",
            "catchphrase-reveal-extends": "both",
        }
        self.settings = Settings(**self.definitions)

    @property
    def actions(self):
        yield Action(
            "cmd", None, "/drama/cmd/", [], "post",
            [Parameter("cmd", True, self.context.validator, [self.context.prompt], ">")],
            "Enter"
        )

    @property
    def active(self):
        return [i for i in self.drama.values() if i.active]

    @property
    def facts(self):
        return {record.name: record.result for record in reversed(self.context.history)}

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    def represent(self, *args, facts=None, previous=None):
        self.context.interlude(
            self.context.folder,
            previous and previous.index,
            previous and previous.ensemble
        )
        presenter = Presenter.build_presenter(
            self.context.folder, *args, facts=facts,
            ensemble=self.context.ensemble + [self.context, self.settings]
        )
        if presenter and not(presenter.dwell or presenter.pause):
            setattr(self.settings, "catchphrase-reveal-extends", "none")
            setattr(self.settings, "catchphrase-states-scrolls", "scroll")
        else:
            setattr(self.settings, "catchphrase-reveal-extends", "both")
            setattr(self.settings, "catchphrase-states-scrolls", "visible")

        return presenter


def parser():
    rv = argparse.ArgumentParser()
    rv.add_argument(
        "--debug", action="store_true", default=False,
        help="Write generated dialogue for debugging."
    )
    rv.add_argument(
        "--quick", action="store_true", default=False,
        help="Don't perform timed animations."
    )
    return rv


def main(opts):
    story = Story(**vars(opts))
    text = None
    presenter = None
    while story.active:
        presenter = story.represent(text, facts=story.context.facts, previous=presenter)
        if opts.debug:
            print(presenter.text, file=sys.stderr)
            print(*presenter.frames, sep="\n", file=sys.stderr)

        for frame in presenter.frames:
            animation = presenter.animate(
                frame, dwell=presenter.dwell, pause=presenter.pause
            )
            if animation is None:
                continue

            try:
                for line, duration in story.render_frame_to_terminal(animation):
                    print(line, "\n")
                    if not opts.quick:
                        time.sleep(duration)
            except TypeError:
                print(story.context.history)
                raise

            if story.context.get_state(Operation) != Operation.frames:
                break

        if story.context.get_state(Operation) == Operation.finish:
            break

        cmd = input("{0} ".format(story.context.prompt))
        text = story.context.deliver(cmd, presenter=presenter)

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
