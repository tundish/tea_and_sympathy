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
            tas.tea.Motivation.paused

.. entity:: KETTLE
   :types:  tas.tea.Space
   :states: tas.tea.Location.hob
            100

.. entity:: DRAMA
   :types:  tas.sympathy.TeaAndSympathy


Thanks
======

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: DRAMA.input_text

.. property:: DRAMA.prompt ?

{0}

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

Served
------

.. condition:: DRAMA.outcomes[served] True

[PLAYER]_

    There you go.

[NPC]_

    Thanks, |PLAYER_NAME|.

.. property:: DRAMA.prompt Well done. You may 'quit' now.

Sugary
------

.. condition:: DRAMA.outcomes[sugary] True

[NPC]_

    Uggh. Sugar.

    Anyway.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name

