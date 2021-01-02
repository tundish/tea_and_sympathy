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

.. entity:: HOB
   :types:  tas.tea.Feature
   :states: tas.tea.Location.HOB
            tas.tea.Acting.passive

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

1
-

.. condition:: KETTLE.state 80

[PLAYER]_

    Here's your tea.

[NPC]_

    Thanks, |PLAYER_NAME|.


.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
