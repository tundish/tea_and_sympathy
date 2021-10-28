:author:    D E Haynes
:made_at:   2021-10-28
:project:   Tea and Sympathy

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Journey.reward
            tas.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Resolution
==========

Doorbell
--------

.. condition:: DRAMA.state 0

Suddenly, across the hall, the doorbell rings.

[NPC]_

    It's Matthew. I've got to go.

[PLAYER]_

    See you later.

    Say hi from me.

.. property:: DRAMA.state 1
.. property:: PLAYER.state tas.types.Location.bedroom

Back to bed
-----------

.. condition:: DRAMA.state 1

|PLAYER_NAME| waits for the front door to shut behind them.
She goes back to her room and puts the mug on the table.

She climbs into bed. As she does, something drops out from under the covers.

She picks it up off the floor, and the screen lights up.

She switches it off for the moment.

.. property:: DRAMA.prompt Press Return
.. property:: DRAMA.state tas.types.Operation.ending

.. |NPC_NAME| property:: NPC.name
.. |PLAYER_NAME| property:: PLAYER.name
