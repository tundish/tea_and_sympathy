.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2020-11-23
:project:   Tea and Sympathy
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: HOB
   :types:  tas.types.Feature
   :states: tas.types.Location.hob
            tas.types.Motivation.paused

.. entity:: KETTLE
   :types:  tas.types.Space
   :states: tas.types.Location.hob
            100

.. entity:: MEDIATOR
   :types:  tas.tea_and_sympathy.TeaAndSympathy


Thanks
======

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: MEDIATOR.input_text

.. property:: MEDIATOR.prompt ?


Brewed
------

.. condition:: MEDIATOR.outcomes[brewed] True

{0}

[PLAYER]_

    Here's your tea.

Untidy
------

.. condition:: MEDIATOR.outcomes[untidy] True

{0}

[NPC]_

    You left the teabag in.

Stingy
------

.. condition:: MEDIATOR.outcomes[stingy] True

{0}

[NPC]_

    We must have run out of milk.

Served
------

.. condition:: MEDIATOR.outcomes[served] True

{0}

[PLAYER]_

    There you go.

[NPC]_

    Thanks, |PLAYER_NAME|.

.. property:: MEDIATOR.prompt Well done. You may 'quit' now.

Sugary
------

.. condition:: MEDIATOR.outcomes[sugary] True

{0}

[NPC]_

    Uggh. Sugar.

    Anyway.

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name

