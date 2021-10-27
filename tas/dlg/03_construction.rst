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

.. If Louise makes the tea, as the kettle boils there are limited options to rescue (default)

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

0
-

.. condition:: GESTURE.state 0

{0}

[PLAYER]_

    Why are you up anyway?

[NPC]_

    I have to go to in to work.

.. property:: GESTURE.state 1

1
-

.. condition:: GESTURE.state 1

{0}

[PLAYER]_

    Are there even any buses?

[NPC]_

    Matthew said he'd take me.

    He's not answering though.

.. property:: GESTURE.state 2

2
-

.. condition:: GESTURE.state 2

{0}

[NPC]_

    I'm gonna be late.

.. property:: GESTURE.state 3

3
-

.. condition:: GESTURE.state 3

{0}

[NPC]_

    What are you doing up then?

[PLAYER]_

    Couldn't sleep.

.. property:: GESTURE.state 4

4
-

.. condition:: GESTURE.state 4

{0}

[NPC]_

    Did you go out?

[PLAYER]_

    Went for drinks after work. So tedious though.

    I wanted an early night.

.. property:: GESTURE.state 5

5
-

.. condition:: GESTURE.state 5

{0}

[PLAYER]_

    You didn't go over to Mattie's then?

[NPC]_

    No.

    He's being very unreliable at the moment.

[PLAYER]_

    Unreliable is about the best you can hope for.

[NPC]_

    Ha ha ha.

.. property:: GESTURE.state 6


6
-

.. condition:: GESTURE.state 6

{0}

[NPC]_

    He's doing his deliveries every night now.

    He's trying to save up some money.

.. property:: GESTURE.state 7

7
-

.. condition:: GESTURE.state 7

{0}

[PLAYER]_

    Maybe he's saving up for a ring.

[NPC]_

    Saving up for another moped, more likely.

.. property:: GESTURE.state 8

8
-

.. condition:: GESTURE.state 8

{0}

[NPC]_

    Kettle's boiling.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
