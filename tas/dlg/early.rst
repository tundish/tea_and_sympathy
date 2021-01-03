.. |VERSION| property:: tas.story.version

:author:    D Haynes
:made_at:   2020-11-23
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.tea.Acting.active

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.tea.Acting.passive

.. entity:: KETTLE
   :types:  tas.tea.Space
   :states: tas.tea.Location.HOB
            20

.. entity:: HOB
   :types:  tas.tea.Feature
   :states: tas.tea.Location.HOB
            tas.tea.Acting.passive

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Early
=====

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: DRAMA.input_text

Caution
-------

.. condition:: DRAMA.turns 0

|NPC_NAME| is on her phone.

[NPC]_

    I am going to swear.

.. property:: DRAMA.prompt Type a command. Do 'quit' if you don't want adult language.

Cold
----

.. condition:: DRAMA.turns 1

[NPC]_

    It's freezing.

.. property:: DRAMA.prompt ?


Spam
----

.. condition:: DRAMA.turns 5

[NPC]_

    Oh God, stop spamming me.

Ignore them
-----------

.. condition:: DRAMA.turns 3

[PLAYER]_

    Just block them.

[NPC]_

    I can't though, it's the Electricity.

Stupidly
--------

.. condition:: DRAMA.turns 5

[NPC]_

    I set it up on my phone.

    Stupidly.

Every day
---------

.. condition:: DRAMA.turns 5

[PLAYER]_

    It's Sunday morning.

[NPC]_

    They are doing it every day now. I swear to God.


Waiting
-------

.. condition:: DRAMA.turns 2

[NPC]_

    Where is he?

Idea
----

.. condition:: DRAMA.turns 2
.. condition:: DRAMA.turns 4

[PLAYER]_

    I'll put the kettle on.

.. property:: DRAMA.prompt ?

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
