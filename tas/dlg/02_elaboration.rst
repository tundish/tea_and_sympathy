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
.. condition:: DRAMA.history[0].name do_propose

|PLAYER_NAME| drops her ash into the bin and goes to the sink.
She starts to wash the blue mug.

[PLAYER]_

    Do you want tea?

[NPC]_

    Yeah sure.

|PLAYER_NAME| moves away to fetch a tea towel.

.. Sophie suggests something.

[NPC]_

    Shall I fill the kettle?

.. property:: GESTURE.state tas.world.Fruition.discussion

No job for Sophie
-----------------

.. condition:: GESTURE.label (\w*\W+tea)
.. condition:: DRAMA.history[0].name do_counter

[PLAYER]_

    Don't worry, I'll do it.

|NPC_NAME| is back on her phone.

[NPC]_

    They are texting me every day now. I swear to God.

.. memory::  1
   :subject: PLAYER
   :object:  NPC

   |NPC_NAME| offers to help with the tea.
   |PLAYER_NAME| would rather she stays out of the way.

.. property:: DRAMA.state 0
.. property:: GESTURE.state tas.world.Fruition.construction

Spark up
--------

.. condition:: GESTURE.label (\w*\W+cig)

|PLAYER_NAME| finds a lighter next to the Kettle, and sparks up.
She takes a saucer from the drainer, and goes over to the window.

Pulling up the sash a little, she looks out through the gap over the garden and to the houses beyond.
She perches herself on the window sill.

.. property:: DRAMA.state 0
.. property:: GESTURE.state tas.world.Fruition.construction

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
