:author:    D E Haynes
:made_at:   2021-10-26
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: GESTURE
   :types:  tas.world.Gesture
   :states: tas.world.Fruition.transition

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Transition
==========

Boredom
-------

.. condition:: GESTURE.label (\w*\W+cig)
.. condition:: NPC.state 0

[PLAYER]_

    Late night out was it?

[NPC]_

    Yeah, you beat me to bed again.

.. property:: DRAMA.state 0
.. property:: DRAMA.state tas.types.Journey.reward
.. property:: GESTURE.state tas.world.Fruition.completion

Distraction
-----------

.. condition:: GESTURE.label (\w*\W+tea)
.. condition:: NPC.state 0
.. condition:: DRAMA.state 0

[PLAYER]_

    Kettle's boiling.

[NPC]_

    Oh yeah, I wasn't paying attention.

    I'll get it.

.. property:: DRAMA.state tas.types.Journey.reward
.. property:: GESTURE.state tas.world.Fruition.completion

Premonition
-----------

.. condition:: NPC.state 1
.. condition:: DRAMA.state 0

|PLAYER_NAME| catches her breath as a sudden insight illuminates her grey morning.

It had felt cold. In the night. At her feet. Then she slept again.

Something very bad is about to happen.

.. property:: DRAMA.state 1
.. property:: GESTURE.abandon drop mug
.. property:: SETTINGS.catchphrase-colour-gravity hsl(203.39, 96.72%, 11.96%);

Last chance
-----------

.. condition:: NPC.state 1
.. condition:: DRAMA.state 1

[NPC]_

    Kettle's boiling.

[PLAYER]_

    I'll get it.

.. property:: DRAMA.state 0
.. property:: GESTURE.state tas.world.Fruition.completion

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
