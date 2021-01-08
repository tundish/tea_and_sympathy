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


Brewed
------

.. condition:: DRAMA.outcomes[brewed] True

[PLAYER]_

    Here's your tea.

Untidy
------

.. condition:: DRAMA.outcomes[untidy] True

[NPC]_

    You left the teabag in.

Stingy
------

.. condition:: DRAMA.outcomes[stingy] True

[NPC]_

    We must have run out of milk.

Sugary
------

.. condition:: DRAMA.outcomes[sugary] True

[NPC]_

    Uggh. Sugar.

Served
------

.. condition:: DRAMA.outcomes[served] True

[PLAYER]_

    There you go.

[NPC]_

    Thanks, |PLAYER_NAME|.

.. property:: DRAMA.prompt Well done. You may 'quit' now.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name

{0}
