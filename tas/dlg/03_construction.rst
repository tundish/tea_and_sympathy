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
   :states: tas.world.Fruition.construction

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Construction
============

Sophie helps out
----------------

.. condition:: GESTURE.label (\w*\W+tea)
.. condition:: DRAMA.history[0].name do_confirm

{0}

[PLAYER]_

    Yeah, if you want to do that.

|NPC_NAME| fills the Kettle at the sink.

.. memory::  0
   :subject: PLAYER
   :object:  NPC

   |NPC_NAME| offers to help with the tea.
   |PLAYER_NAME| doesn't feel like arguing this morning.

.. If Louise makes the tea, as the kettle boils there are limited options to rescue (default)
.. Otherwise, more chat about Mattie.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
