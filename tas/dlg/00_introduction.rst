:author:    D E Haynes
:made_at:   2021-10-20
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: KETTLE
   :types:  tas.types.Container
   :states: tas.types.Availability.fixture

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Availability.allowed

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.mentor
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Introduction
============

Open
----

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 0

There is a thud. From above.

|PLAYER_NAME| sits up in bed. She listens for a moment, confused.

Then looks toward the door.

.. property:: DRAMA.prompt Type 'help'. Or 'again' to read once more.
.. property:: DRAMA.state 1

Listen
------

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 1

{0}

|PLAYER_NAME| listens for a moment.
Someone is moving around the house.

.. property:: DRAMA.prompt Type a command or just Return to continue.
.. property:: DRAMA.state 2

Shiver
------

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 2

{0}

|PLAYER_NAME| hugs herself defensively.
It's cold. And it's early.

.. property:: DRAMA.state 1

.. Hallway
.. Kitchen
.. Sophie


.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
