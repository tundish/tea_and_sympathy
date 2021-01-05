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


import argparse
from collections import deque
import sys

from aiohttp import web
import pkg_resources

from turberfield.catchphrase.presenter import Presenter

import tas
from tas.story import Story


async def get_frame(request):
    story = request.app["story"][0]
    try:
        animation = None
        while not animation:
            frame = story.presenter.frames.pop(0)
            animation = story.presenter.animate(frame)
    except (AttributeError, IndexError):
        story.drama.input_text = ""
        n, story.presenter = Presenter.build_from_folder(
            folder=story.drama.folder,
            ensemble=story.drama.ensemble + [story.settings],
            strict=True
        )
        frame = story.presenter.frames.pop(0)
        animation = story.presenter.animate(frame)

    refresh = Presenter.refresh_animations(animation, min_val=2) if story.presenter.pending else None
    refresh_target = story.refresh_target("/")
    title = next(iter(story.presenter.metadata.get("project", ["Tea and Sympathy"])), "Tea and Sympathy")
    rv = story.render_body_html(title=title, next_=refresh_target, refresh=refresh).format(
        '<link rel="stylesheet" href="/css/theme/tas.css" />',
        story.render_dict_to_css(vars(story.settings)),
        story.render_frame_to_html(
            animation,
            options=story.drama.active,
            prompt=story.drama.prompt, title=title,
            commands=not story.presenter.pending,
        )
    )
    return web.Response(text=rv, content_type="text/html")


async def post_command(request):
    story = request.app["story"][0]
    data = await request.post()
    cmd = data["cmd"]
    if not story.drama.validator.match(cmd):
        raise web.HTTPUnauthorized(reason="User sent invalid command.")
    else:
        fn, args, kwargs = story.drama.interpret(story.drama.match(cmd))
        results = story.drama(fn, *args, **kwargs)
        n, story.presenter = Presenter.build_from_folder(
            *Presenter.build_shots(*results, shot="Epilogue"),
            folder=story.drama.folder,
            ensemble=story.drama.ensemble + [story.settings],
            strict=True
        )
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
    story = Story()
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
