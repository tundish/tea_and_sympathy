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
   :states: tas.world.Fruition.discussion

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Discussion
==========

Make Tea
--------

.. condition:: GESTURE.label (\w*\W+tea)

|PLAYER_NAME| senses rivalry for control of the Kitchen.
She doesn't want to add to the drama.

But an answer is required.

[NPC]_

    Shall I fill the kettle?


.. property:: GESTURE.counter no
.. property:: GESTURE.confirm yes

.. Ask her about Mattie (discussion) or just go ahead and make the tea (construction).
.. a minor squabble results in Sophie making the tea instead (construction).

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
