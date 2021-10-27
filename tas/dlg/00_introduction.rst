:author:    D E Haynes
:made_at:   2021-10-20
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Availability.allowed

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.mentor
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Introduction
============

Open
----

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 0

There is a thud. From above.

|PLAYER_NAME| sits up in bed. She listens for a moment, confused.

Then looks toward the door.

.. property:: DRAMA.prompt Type 'help'. Or 'again' to read once more.
.. property:: DRAMA.state 1

Listen
------

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 1

{0}

|PLAYER_NAME| listens for a moment.
She's not alone in the house. Is there going to be a problem?

.. property:: DRAMA.prompt Type a command to continue.
.. property:: DRAMA.state 2

Shiver
------

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 2

{0}

|PLAYER_NAME| hugs herself defensively.
It's cold. And it's early.

.. property:: DRAMA.state 1

Hallway
-------

.. condition:: PLAYER.state tas.types.Location.hall
.. condition:: DRAMA.state 0

There is the squeak of a door.

From semi-darkness, the bare floor is suddenly bathed in tobacco and tungsten.

|PLAYER_NAME|, in her blue cotton pyjamas, stumbles clumsily into the hallway.

.. property:: DRAMA.state 1
.. property:: DRAMA.prompt To wait for a moment, simply hit Return.

Between
-------

.. condition:: PLAYER.state tas.types.Location.hall
.. condition:: DRAMA.state 1

{0}

|PLAYER_NAME| lets the empty space soothe her for a moment.
Everywhere else there are situations.

.. property:: DRAMA.state 2

Sunday
------

.. condition:: PLAYER.state tas.types.Location.hall
.. condition:: DRAMA.state 2

{0}

|PLAYER_NAME| wonders what she's doing up so early on a Sunday.

.. property:: DRAMA.state 1

Kitchen
-------

.. condition:: PLAYER.state tas.types.Location.kitchen
.. condition:: DRAMA.state 0

{0}

The Kitchen is less gloomy than the rest of the house.
It has mostly white walls. The shaky cupboards were painted white too, several years ago.

**Sophie** has her boots on the table.

.. property:: DRAMA.state 1
.. property:: DRAMA.prompt ?

Sophie
------

.. condition:: PLAYER.state tas.types.Location.kitchen
.. condition:: DRAMA.state 1

{0}

|NPC_NAME| is on her phone.

[NPC]_

    I am going to swear.

.. property:: DRAMA.state 2

Phone
-----

.. condition:: PLAYER.state tas.types.Location.kitchen
.. condition:: DRAMA.state 2

[NPC]_

    Oh God, stop spamming me.

{0}

[PLAYER]_

    Just block them.

[NPC]_

    I can't though, it's the Electricity.
    You have to have it so you can pay.

    I'm trying to get hold of Matthew.

.. property:: DRAMA.state 0
.. property:: DRAMA.state tas.types.Journey.ordeal

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
