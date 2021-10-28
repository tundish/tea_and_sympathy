:author:    D E Haynes
:made_at:   2021-10-27
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: GESTURE
   :types:  tas.world.Gesture
   :states: tas.world.Fruition.completion

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Completion
==========

Denouement
----------

|NPC_NAME| looks up from her phone to meet the frightened face of |PLAYER_NAME|.
Through the open door, a musical ring tone is clearly to be heard coming from her room.

In the Kitchen at first there is silence.

[PLAYER]_

    |NPC_NAME|...

Then across the hall, the doorbell rings.

.. property:: DRAMA.state 0
.. property:: DRAMA.prompt Press Return
.. property:: DRAMA.state tas.types.Operation.ending

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
