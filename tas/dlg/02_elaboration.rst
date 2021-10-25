:author:    D E Haynes
:made_at:   2021-10-25
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: GESTURE
   :types:  tas.world.Gesture
   :states: tas.world.Fruition.elaboration

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Elaboration
===========

Make Tea
--------

.. condition:: GESTURE.label (\w*\W+tea)

|PLAYER_NAME| drops her ash into the bin and goes to the sink.
She starts to wash the blue mug.

[PLAYER]_

    Do you want tea?

[NPC]_

    Er, yeah sure.

|PLAYER_NAME| moves away to fetch a tea towel.

[NPC]_

    Shall I fill the kettle?

.. Sophie counters. Go to discussion
.. property:: GESTURE.state tas.world.Fruition.discussion


Spark up
--------

.. condition:: GESTURE.label (\w*\W+cig)

About to make smoke then.

.. Sophie getting uncomfortable. She doesn't like smoke (cancelled).

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
