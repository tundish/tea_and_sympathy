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

Sophie
------

.. condition:: DRAMA.state 0

{0}

Elaboration.

|NPC_NAME| has her boots on the table.

.. property:: DRAMA.state 1

.. Sophie getting uncomfortable. She doesn't like smoke (cancelled).
.. Ask her about Mattie (discussion) or just go ahead and make the tea (construction).
