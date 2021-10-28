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

[PLAYER]_

    Yes, if you want to do that. I suppose.

|NPC_NAME| fills the Kettle at the sink.

.. memory::  0
   :subject: PLAYER
   :object:  NPC

   |NPC_NAME| offers to help with the tea.
   |PLAYER_NAME| doesn't feel like arguing this morning.

.. property:: DRAMA.state 0

0
-

.. condition:: DRAMA.state 0

{0}

[PLAYER]_

    Why are you up anyway?

[NPC]_

    I have to go in to college.

.. property:: DRAMA.state 1
.. property:: DRAMA.state tas.types.Operation.frames

1
-

.. condition:: DRAMA.state 1

[PLAYER]_

    On a Sunday?

[NPC]_

    It's the only time I can use the kiln.

[PLAYER]_

    How are you going to get there?

[NPC]_

    Matthew said he'd take me.

    He's not answering though.

.. property:: DRAMA.state 2
.. property:: DRAMA.state tas.types.Operation.prompt

2
-

.. condition:: DRAMA.state 2
.. condition:: GESTURE.label (\w*\W+cig)

|PLAYER_NAME| nods.

Glances out to the garden again.

.. memory::  0
   :subject: PLAYER
   :object:  NPC

   |NPC_NAME| is panicking about getting to college.
   |PLAYER_NAME| is not really in the mood for talking.

.. property:: DRAMA.state 0
.. property:: GESTURE.state tas.world.Fruition.transition

3
-

.. condition:: DRAMA.state 2
.. condition:: GESTURE.label (\w*\W+tea)

{0}

[NPC]_

    I'm gonna be late.

    He'd better have a good excuse.

.. property:: DRAMA.state 4
.. property:: DRAMA.state tas.types.Operation.frames

4
-

.. condition:: DRAMA.state 4

[PLAYER]_

    I didn't know where you were last night.

    Did you go out?

[NPC]_

    Film festival. Not great though.

    So another late one.

.. property:: DRAMA.state 5
.. property:: DRAMA.state tas.types.Operation.prompt

5
-

.. condition:: DRAMA.state 5

{0}

[PLAYER]_

    You didn't see Mattie then?

[NPC]_

    No.

    He's being very unreliable at the moment.

[PLAYER]_

    Unreliable is about the best you can hope for.

|NPC_NAME| does not see the funny side.

.. property:: DRAMA.state 6


6
-

.. condition:: DRAMA.state 6

{0}

[NPC]_

    He's doing his deliveries every night now.

    He's trying to save up some money.

    He says he's giving up smoking but I don't believe him.

.. property:: DRAMA.state 8

8
-

.. condition:: DRAMA.state 8

[PLAYER]_

    Is he working this morning?

[NPC]_

    Not usually.

    I'll have to try his deliveries number.

.. property:: DRAMA.state 9
.. property:: DRAMA.state tas.types.Operation.prompt

9
-

.. condition:: DRAMA.state 9

[NPC]_

    He hates it when I call him on his work phone.

    Anyway. He'd better answer this time.

.. property:: DRAMA.state 0
.. property:: GESTURE.state tas.world.Fruition.transition


.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
