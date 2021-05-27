.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2020-11-23
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.tea.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.tea.Motivation.acting

.. entity:: KETTLE
   :types:  tas.tea.Space
   :states: tas.tea.Location.hob
            20

.. entity:: HOB
   :types:  tas.tea.Feature
   :states: tas.tea.Location.hob
            tas.tea.Motivation.paused

.. entity:: MEDIATOR
   :types:  tas.sympathy.TeaAndSympathy

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Early
=====

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: MEDIATOR.input_text

Caution
-------

.. condition:: MEDIATOR.turns 0

|NPC_NAME| is on her phone.

[NPC]_

    I am going to swear.

.. property:: MEDIATOR.prompt Type 'help'. Or 'quit' if you don't want adult language.

Cold
----

.. condition:: MEDIATOR.turns 1

[NPC]_

    It's freezing.

.. property:: MEDIATOR.prompt ?


Spam
----

.. condition:: MEDIATOR.turns 2

[NPC]_

    Oh God, stop spamming me.

Ignore them
-----------

.. condition:: MEDIATOR.turns 3

[PLAYER]_

    Just block them.

[NPC]_

    I can't though, it's the Electricity.

Idea
----

.. condition:: MEDIATOR.turns 4

[PLAYER]_

    I'll put the kettle on.


Stupidly
--------

.. condition:: MEDIATOR.turns 5

[NPC]_

    I set it up on my phone.

    Stupidly.

Every day
---------

.. condition:: MEDIATOR.turns 6

[PLAYER]_

    It's Sunday morning.

[NPC]_

    They are doing it every day now. I swear to God.

Calm
----

.. condition:: MEDIATOR.turns 7

[PLAYER]_

    I'll put the kettle on.


Waiting
-------

.. condition:: MEDIATOR.turns 8

[NPC]_

    Where is he?

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name

Mediation
---------

{0}
