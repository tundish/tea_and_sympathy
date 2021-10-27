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

    Yes, if you want to do that. I suppose.

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

    I have to go in to college.

.. property:: GESTURE.state 1
.. property:: DRAMA.state tas.types.Operation.frames

1
-

.. condition:: GESTURE.state 1

[PLAYER]_

    On a Sunday?

[NPC]_

    It's the only time I can use the kiln.

[PLAYER]_

    How are you going to get there?

[NPC]_

    Matthew said he'd take me.

    He's not answering though.

.. property:: GESTURE.state 2
.. property:: DRAMA.state tas.types.Operation.prompt

2
-

.. condition:: GESTURE.state 2

{0}

[NPC]_

    I'm gonna be late.

    He'd better have a good excuse.

.. property:: GESTURE.state 3
.. property:: DRAMA.state tas.types.Operation.frames

3
-

.. condition:: GESTURE.state 3

[NPC]_

    What are you doing up then?

[PLAYER]_

    Couldn't sleep.

.. property:: GESTURE.state 4
.. property:: DRAMA.state tas.types.Operation.prompt

4
-

.. condition:: GESTURE.state 4

{0}

[PLAYER]_

    I didn't know where you were last night.

    Did you go out?

[NPC]_

    Film festival. Not great though.

    I wanted an early night.

.. property:: GESTURE.state 5

5
-

.. condition:: GESTURE.state 5

{0}

[PLAYER]_

    You didn't see Mattie then?

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

    He says he's giving up smoking but I don't believe him.

.. property:: GESTURE.state 7

7
-

.. condition:: GESTURE.state 7

{0}

[PLAYER]_

    Maybe he's getting a ring.

[NPC]_

    Getting a bigger moped.

    But I want go on holiday this year.

.. property:: GESTURE.state 8
.. property:: DRAMA.state tas.types.Operation.frames

8
-

.. condition:: GESTURE.state 8

{0}

[PLAYER]_

    Is he working this morning?

[NPC]_

    Not usually.

    I'll have to try his deliveries number.

.. property:: GESTURE.state 9

9
-

.. condition:: GESTURE.state 9

[NPC]_

    He hates it when I call him on his work phone.

    Anyway. He'd better answer this time.

.. property:: GESTURE.state Fruition.transition
.. property:: DRAMA.state tas.types.Operation.prompt


.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
