.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-01-10
:project:   Tea and Sympathy
:version:   |VERSION|
:dwell:     0
:pause:     0

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.tea.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.tea.Motivation.paused

.. entity:: DRAMA
   :types:  tas.sympathy.TeaAndSympathy

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Paused
======

Help
----

.. condition:: DRAMA.history[0].args[0] help

[DRAMA]_

    You are woken early one Sunday morning.
    Your flatmate is up and anxious.
    Maybe you could make her a cup of tea.

{help_examples}

[DRAMA]_

    Start with a *look around*.
    The character dialogue may give you some hints.
    To see how things are coming along, you can *check* an object.
    To see a list of past actions, use the *history* command.

.. property:: DRAMA.prompt ?
.. property:: NPC.state tas.tea.Motivation.acting
.. property:: SETTINGS.catchphrase-colour-gravity hsl(209.33, 96.92%, 12.75%)
