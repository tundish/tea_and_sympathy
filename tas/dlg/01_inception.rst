:author:    D E Haynes
:made_at:   2021-10-20
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: OPTION_1
   :types:  tas.world.Gesture
   :states: tas.world.Fruition.inception

.. entity:: OPTION_2
   :types:  tas.world.Gesture
   :states: tas.world.Fruition.inception

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Location.inventory

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.ordeal
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Inception
=========

Sophie
------

.. condition:: DRAMA.state 0

{0}

|NPC_NAME| has her boots on the table.

Her long black hair is a bit tangled, but sometimes she does that on purpose.

.. property:: NPC.description   |PLAYER_NAME| notices she is wearing her best outfit.
                                A long-sleeved black fishnet top, and a leather bodice.
                                Black woollen miniskirt and leggings.

.. property:: DRAMA.state 1
.. property:: OPTION_1.state tas.types.Availability.allowed
.. property:: OPTION_2.state tas.types.Availability.allowed

Options
-------

.. condition:: DRAMA.state 1

{0}

|PLAYER_NAME| considers whether |PLAYER_SUBJECT| should |OPTION_1_IMPERATIVE| |OPTION_1_ARTICLE| |OPTION_1_NOUN|,
or maybe |OPTION_2_IMPERATIVE| |OPTION_2_ARTICLE| |OPTION_2_NOUN| instead.


.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
.. |PLAYER_SUBJECT| property:: PLAYER.names[0].pronoun.subject
.. |OPTION_1_IMPERATIVE| property:: OPTION_1.head.propose[0].verb.imperative
.. |OPTION_1_ARTICLE| property:: OPTION_1.head.propose[0].name.article.indefinite
.. |OPTION_1_NOUN| property:: OPTION_1.head.propose[0].name.noun
.. |OPTION_2_IMPERATIVE| property:: OPTION_2.head.propose[0].verb.imperative
.. |OPTION_2_ARTICLE| property:: OPTION_2.head.propose[0].name.article.definite
.. |OPTION_2_NOUN| property:: OPTION_2.head.propose[0].name.noun
