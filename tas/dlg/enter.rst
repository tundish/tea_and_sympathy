.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-05-10
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.teatime.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.teatime.Motivation.acting

.. entity:: DRAMA
   :types:  tas.sympathy.Sympathy
   :states: tas.teatime.Operation.normal

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

Enter
=====

Curtain
-------

The hallway is in half darkness.

Now the squeak of a door.

The floor bathes in tobacco and tungsten.

|PLAYER_NAME| wears warm pyjamas. She pads clumsily past the stairs to
the kitchen.


.. property:: DRAMA.state tas.teatime.Operation.ending

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
