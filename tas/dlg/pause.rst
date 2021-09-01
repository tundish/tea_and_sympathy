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
   :states: tas.teatime.Motivation.paused

.. entity:: MEDIATOR
   :types:  tas.tea_and_sympathy.TeaAndSympathy

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Paused
======

Help
----

.. condition:: MEDIATOR.history[0].name do_help

[MEDIATOR]_

    You are woken early one Sunday morning.
    Your flatmate is up and anxious.
    Maybe you could make her a cup of tea.

{do_help}

[MEDIATOR]_

    Start with a *look around*.
    The character dialogue may give you some hints.
    To see how things are coming along, you can *check* an object.
    To see a list of past actions, use the *history* command.

.. property:: MEDIATOR.prompt ?
.. property:: NPC.state tas.teatime.Motivation.acting

Look
----

.. condition:: MEDIATOR.history[0].name do_look

[MEDIATOR]_

    Looking around, you see:

{do_look}

.. property:: MEDIATOR.prompt ?
.. property:: NPC.state tas.teatime.Motivation.acting
