.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-10-05
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: MUG
   :types:  tas.types.Container

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.mentor
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Enter
=====

Curtain
-------

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 0

A thud. From above.

|PLAYER_NAME| sits up in bed. She listens for a moment, confused.

Then looks towards the door.

.. property:: DRAMA.prompt Type 'help'. Or 'again' to read once more.
.. property:: DRAMA.state 1

Intro
-----

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 1

{0}

Someone is moving around the house.

.. property:: DRAMA.state 2

End
---

.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: DRAMA.state 2

{0}

It's cold. And it's early.

.. property:: DRAMA.state 1

Hallway
-------

.. condition:: PLAYER.state tas.types.Location.hall
.. condition:: DRAMA.state 0

The hallway is in half darkness.

Now the squeak of a door.

The bare floor bathes in tobacco and tungsten.

|PLAYER_NAME|, in pyjamas, pads clumsily past the stairs to
the kitchen.

.. property:: DRAMA.state 1

Hesitation
----------

.. condition:: PLAYER.state tas.types.Location.hall
.. condition:: DRAMA.state 1

{0}

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
