.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-09-03
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: DRAMA
   :types:  tas.sympathy.Sympathy
   :states: tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Early
=====

Filling
-------

.. condition:: DRAMA.p.trace[1] pro_filling
.. condition:: DRAMA.p.trace[0] pro_missing

{0}


|PLAYER_NAME| fills the kettle.

Caution
-------

.. condition:: DRAMA.turns 0

{0}

|NPC_NAME| is on her phone.

[NPC]_

    I am going to swear.

.. property:: DRAMA.prompt Type 'help'. Or 'quit' if you don't want adult language.

Cold
----

.. condition:: DRAMA.turns 1

{0}

[NPC]_

    It's freezing.

.. property:: DRAMA.prompt ?


Spam
----

.. condition:: DRAMA.turns 2

{0}

[NPC]_

    Oh God, stop spamming me.

Ignore them
-----------

.. condition:: DRAMA.turns 3

{0}

[PLAYER]_

    Just block them.

[NPC]_

    I can't though, it's the Electricity.

Idea
----

.. condition:: DRAMA.turns 4

{0}

[PLAYER]_

    I'll put the kettle on.


Stupidly
--------

.. condition:: DRAMA.turns 5

{0}

[NPC]_

    I set it up on my phone.

    Stupidly.

Every day
---------

.. condition:: DRAMA.turns 6

{0}

[PLAYER]_

    It's Sunday morning.

[NPC]_

    They are doing it every day now. I swear to God.


Waiting
-------

.. condition:: DRAMA.turns 8

{0}

[NPC]_

    Where is he?

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
