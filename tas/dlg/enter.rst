.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-05-10
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: DRAMA
   :types:  tas.sympathy.Sympathy
   :states: tas.types.Operation.normal

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

Enter
=====

Curtain
-------

.. condition:: DRAMA.state 0

The hallway is in half darkness.

Now the squeak of a door.

The bare floor bathes in tobacco and tungsten.

|PLAYER_NAME| wears warm pyjamas. She pads clumsily past the stairs to
the kitchen.

.. property:: DRAMA.prompt Type 'help'. Or 'again' to read once more.
.. property:: DRAMA.state 1

Intro
-----

.. condition:: DRAMA.state 1

I wonder...?

.. property:: DRAMA.state 2

End
---

.. condition:: DRAMA.state 2

Bye.

.. property:: DRAMA.state tas.teatime.Operation.paused
.. property:: DRAMA.state 3

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
