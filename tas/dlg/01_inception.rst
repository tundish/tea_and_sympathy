:author:    D E Haynes
:made_at:   2021-10-20
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player
            tas.types.Location.kitchen

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: KETTLE
   :types:  tas.types.Container
   :states: tas.types.Availability.fixture

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Inception
=========

Sophie
------

.. condition:: DRAMA.state 0
.. condition:: PLAYER.state tas.types.Location.kitchen

{0}

|NPC_NAME| has her boots on the table.

|PLAYER_NAME| notices she is wearing her best outfit.
A long-sleeved black fishnet top, and a leather bodice. Black woollen miniskirt and leggings.

Her long black hair is a bit tangled, but sometimes she does that on purpose.

.. Smoke cigarette
.. Make tea

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
