.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-01-10
:project:   Tea and Sympathy
:version:   |VERSION|
:dwell:     0.2
:pause:     1

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.teatime.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.teatime.Motivation.acting

.. entity:: DRAMA
   :types:  tas.sympathy.Sympathy
   :states: tas.teatime.Operation.ending

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


About
=====

Info
----

.. property:: SETTINGS.catchphrase-colour-gravity hsl(113.33, 96.92%, 12.75%)
.. property:: SETTINGS.catchphrase-reveal-extends both

This is a technical demo and teaching example for the `turberfield-catchphrase`_ package.
A modern, web-native Python library you can download and install today. It's there_ for you to use.

Catchphrase is unique in the way it lets you layer beautifully-written dialogue on top of well-tested game logic.
Your Interactive Story will be a work of art, and at the same time a nice piece of engineering.

*   Catchphrase is 100% Free software.
*   Your game logic is Python code.
*   Character dialogue lives in separate screenplay files.
*   Catchphrase renders your story in pure HTML5 and CSS3. No Javascript is necessary.
*   Host Web mode for a browser interface or play old-school in the terminal.

© 2021 D E Haynes.

Why not `see how it's done`_?

.. property:: DRAMA.state tas.teatime.Operation.finish

.. _turberfield-catchphrase: https://github.com/tundish/turberfield-catchphrase
.. _there: https://pypi.org/project/turberfield-catchphrase/
.. _see how it's done: https://github.com/tundish/tea-and-sympathy

