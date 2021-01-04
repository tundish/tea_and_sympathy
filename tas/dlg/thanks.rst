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
            100

.. entity:: MUG
   :types:  tas.tea.Space
   :states: tas.tea.Location.COUNTER

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Thanks
======

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: DRAMA.input_text

.. property:: DRAMA.prompt ?

1
-

[PLAYER]_

    Here's your tea.

[NPC]_

    Thanks, |PLAYER_NAME|.

Sloppy
------

.. condition:: MUG.state tas.tea.Location.COUNTER

[NPC]_

    You left the teabag in.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
