.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-01-10
:project:   Tea and Sympathy
:version:   |VERSION|
:dwell:     0
:pause:     0

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.teatime.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.teatime.Motivation.acting

.. entity:: MUG
   :types:  tas.types.Container

.. entity:: DRAMA
   :types:  tas.sympathy.Sympathy
   :states: tas.teatime.Operation.paused

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Paused
======

Help
----

.. condition:: DRAMA.history[0].name do_help

[DRAMA]_

    You are woken early one Sunday morning.
    Your flatmate is up and anxious.

    It doesn't hurt to *look around*.
    The dialogue may give you hints too.
    Here are some commands to try:

{0}

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.teatime.Operation.normal

History
-------

.. condition:: DRAMA.history[0].name do_history

[DRAMA]_

    Recent commands:

{0}

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.teatime.Operation.normal

See Mug in Bedroom
------------------

.. condition:: DRAMA.history[0].name do_look
.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: MUG.state tas.types.Location.bedroom

[DRAMA]_

    |PLAYER_NAME| is in the |PLAYER_LOCN|.

    The curtains are closed.
    A vertical strip of early grey light makes a mist of stale exhalation.

    Next to the bed is a tatty old table, and on it a ceramic mug.

    The door is shut. Beyond it is a hallway.

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.teatime.Operation.normal

Inspect
-------

.. condition:: DRAMA.history[0].name do_inspect

[DRAMA]_

    |INPUT_TEXT|

{0}


Look
----

.. condition:: DRAMA.history[0].name do_look

[DRAMA]_

    |PLAYER_NAME| is in the |PLAYER_LOCN|.
    Looking around, she is aware of:

{0}

.. |INPUT_TEXT| property:: DRAMA.input_text
.. |PLAYER_NAME| property:: PLAYER.name
.. |PLAYER_LOCN| property:: PLAYER.location.title
