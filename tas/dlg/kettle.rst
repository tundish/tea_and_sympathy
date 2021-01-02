.. |VERSION| property:: tas.story.version

:author:    D Haynes
:made_at:   2020-11-23
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.tea.Acting.active

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.tea.Acting.passive

.. entity:: KETTLE
   :types:  tas.tea.Space
   :states: tas.tea.Location.HOB

.. entity:: HOB
   :types:  tas.tea.Feature
   :states: tas.tea.Location.HOB
            tas.tea.Acting.active

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Boiling
=======

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: DRAMA.input_text


1
-

.. condition:: KETTLE.state 20

[PLAYER]_

    Why are you up anyway?

[NPC]_

    I've got work.

    I have to go to work.

[PLAYER]_

    Oh |NPC_NAME|, that's shit.

2
-

.. condition:: KETTLE.state 30

[PLAYER]_

    Are there even any buses?

[NPC]_

    Matthew said he'd take me.

    He's not answering though.

5
-

.. condition:: KETTLE.state 40

[NPC]_

    I'm gonna be late.

    Bollocks to it.

6
-

.. condition:: KETTLE.state 50

[NPC]_

    What are you doing up then?

[PLAYER]_

    Couldn't sleep.

[NPC]_

    Did you go out?

[PLAYER]_

    Went for drinks after work. So tedious though.

    I wanted an early night.

7
-

.. condition:: KETTLE.state 60

[PLAYER]_

    You didn't go over to Mattie's then?

[NPC]_

    No.

    He's being very unreliable at the moment.

[PLAYER]_

    Unreliable is about the best you can hope for.

[NPC]_

    Ha ha ha.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
