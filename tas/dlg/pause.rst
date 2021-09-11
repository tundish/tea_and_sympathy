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
    Maybe you could make her a cup of tea.

{do_help}

[DRAMA]_

    Start with a *look around*.
    The character dialogue may give you some hints.
    To see how things are coming along, you can *check* an object.
    To see a list of past actions, use the *history* command.

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.teatime.Operation.normal

Look
----

.. condition:: DRAMA.history[0].name do_look

[DRAMA]_

    Looking around, you see:

{do_look}

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.teatime.Operation.normal
