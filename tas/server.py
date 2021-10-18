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


import argparse
from collections import deque
import sys

from aiohttp import web
import pkg_resources

from turberfield.catchphrase.presenter import Presenter

import tas
from tas.story import TeaAndSympathy
from tas.types import Operation


async def get_frame(request):
    story = request.app["story"][0]

    while story.presenter.frames:
        frame = story.presenter.frames.pop(0)
        animation = story.presenter.animate(
            frame,
            dwell=story.presenter.dwell,
            pause=story.presenter.pause
        )
        if animation:
            story.animation = animation
            break

    if story.context.get_state(Operation) == Operation.frames:
        refresh = Presenter.refresh_animations(story.animation, min_val=2)
        refresh_target = story.refresh_target("/")
    else:
        refresh = None
        refresh_target = None

    title = next(iter(story.presenter.metadata.get("project", ["Tea and Sympathy"])), "Tea and Sympathy")
    controls = [
        "\n".join(story.render_action_form(action, autofocus=not n))
        for n, action in enumerate(story.actions)
        if story.context.get_state(Operation) not in (Operation.finish, Operation.frames)
    ]
    rv = story.render_body_html(title=title, next_=refresh_target, refresh=refresh).format(
        '<link rel="stylesheet" href="/css/theme/tas.css" />',
        story.render_dict_to_css(vars(story.settings)),
        story.render_animated_frame_to_html(story.animation, controls)
    )

    return web.Response(text=rv, content_type="text/html")


async def post_command(request):
    story = request.app["story"][0]
    data = await request.post()
    cmd = data["cmd"]
    if not story.context.validator.match(cmd):
        raise web.HTTPUnauthorized(reason="User sent invalid command.")
    else:
        text = story.context.deliver(cmd, presenter=story.presenter)
        story.presenter = story.represent(text, facts=story.context.facts, previous=story.presenter)
    raise web.HTTPFound("/")


def build_app(args):
    app = web.Application()
    app.add_routes([
        web.get("/", get_frame),
        web.post("/drama/cmd/", post_command),
    ])
    app.router.add_static(
        "/css/base/",
        pkg_resources.resource_filename("turberfield.catchphrase", "css")
    )
    app.router.add_static(
        "/css/theme/",
        pkg_resources.resource_filename("tas", "css")
    )
    story = TeaAndSympathy(**vars(args))
    story.presenter = story.represent("", facts=story.context.facts)
    app["story"] = deque([story], maxlen=1)
    return app


def main(args):
    app = build_app(args)
    return web.run_app(app, host=args.host, port=args.port)


def parser(description=__doc__):
    rv = argparse.ArgumentParser(description)
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number.")
    rv.add_argument(
        "--host", default="127.0.0.1",
        help="Set an interface on which to serve."
    )
    rv.add_argument(
        "--port", default=8080, type=int,
        help="Set a port on which to serve."
    )
    return rv


def run():
    p = parser()
    args = p.parse_args()

    rv = 0
    if args.version:
        sys.stdout.write(tas.__version__)
        sys.stdout.write("\n")
    else:
        rv = main(args)

    if rv == 2:
        sys.stderr.write("\n Missing command.\n\n")
        p.print_help()

    sys.exit(rv)


if __name__ == "__main__":
    run()
