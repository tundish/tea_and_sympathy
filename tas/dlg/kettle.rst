.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2020-11-23
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.tea.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.tea.Motivation.acting

.. entity:: HOB
   :types:  tas.tea.Feature
   :states: tas.tea.Location.hob
            tas.tea.Motivation.acting

.. entity:: KETTLE
   :types:  tas.tea.Space
   :states: tas.tea.Location.hob

.. entity:: MEDIATOR
   :types:  tas.sympathy.TeaAndSympathy

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Boiling
=======

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: MEDIATOR.input_text


.. property:: MEDIATOR.prompt ?
.. property:: SETTINGS.catchphrase-reveal-extends both

1
-

.. condition:: KETTLE.state 20

{0}

[PLAYER]_

    Why are you up anyway?

[NPC]_

    I have to go to in to work.

[PLAYER]_

    Oh |NPC_NAME|, that's shit.

2
-

.. condition:: KETTLE.state 30

{0}

[PLAYER]_

    Are there even any buses?

[NPC]_

    Matthew said he'd take me.

    He's not answering though.

3
-

.. condition:: KETTLE.state 40

{0}

[NPC]_

    I'm gonna be late.

    Bollocks to it.

4
-

.. condition:: KETTLE.state 50

{0}

[NPC]_

    What are you doing up then?

[PLAYER]_

    Couldn't sleep.

5
-

.. condition:: KETTLE.state 60

{0}

[NPC]_

    Did you go out?

[PLAYER]_

    Went for drinks after work. So tedious though.

    I wanted an early night.

6
-

.. condition:: KETTLE.state 70

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


7
-

.. condition:: KETTLE.state 80

{0}

[NPC]_

    He's doing his deliveries every night now.

    He's trying to save up some money.

8
-

.. condition:: KETTLE.state 90

{0}

[PLAYER]_

    Maybe he's saving up for a ring.

[NPC]_

    Saving up for another moped, more likely.

9
-

.. condition:: KETTLE.state 100

{0}

[NPC]_

    Kettle's boiling.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
