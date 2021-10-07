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

{0}

[DRAMA]_

    Start with a *look around*.
    The character dialogue may give you some hints.
    To see a list of past actions, use the *history* command.

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

Look
----

.. condition:: DRAMA.history[0].name do_look

[DRAMA]_

    |PLAYER_NAME| is in the |PLAYER_LOCN|.
    Looking around, she sees:

{0}

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.teatime.Operation.normal

.. |PLAYER_NAME| property:: PLAYER.name
.. |PLAYER_LOCN| property:: PLAYER.location.title
