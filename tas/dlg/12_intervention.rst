:author:    D E Haynes
:made_at:   2021-10-20
:project:   Tea and Sympathy
:dwell:     0
:pause:     0

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.types.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.types.Motivation.acting

.. entity:: KETTLE
   :types:  tas.types.Container
   :states: tas.types.Availability.fixture

.. entity:: MUG
   :types:  tas.types.Container
   :states: tas.types.Availability.allowed

.. entity:: DRAMA
   :types:  tas.drama.Sympathy
   :states: tas.types.Operation.paused

.. entity:: SETTINGS
   :types:  balladeer.Settings

Intervention
============

Help
----

.. condition:: DRAMA.history[0].name do_help

[DRAMA]_

    Louise wakes early one Sunday morning.
    Her flatmate is already up.

    The dialogue may give you hints on what you might wish to do.
    Here are some commands to try:

{0}

[DRAMA]_

    You can always choose to do nothing, simply by pressing *Return*.

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state tas.types.Operation.prompt

History
-------

.. condition:: DRAMA.history[0].name do_history

[DRAMA]_

    Recent commands:

{0}

.. property:: DRAMA.state tas.types.Operation.prompt

See Mug in Bedroom
------------------

.. condition:: DRAMA.history[0].name do_look
.. condition:: PLAYER.state tas.types.Location.bedroom
.. condition:: MUG.state tas.types.Location.bedroom

[DRAMA]_

    |PLAYER_NAME| is in the |PLAYER_LOCN|.

    The curtains are closed.
    A vertical strip of early grey light makes a mist of stale exhalations.

    Next to the bed is a tatty old table, and on it a ceramic **mug**.

    The door is shut. Beyond it is a **hallway**.

    |PLAYER_NAME| sees:

{0}

.. property:: DRAMA.state tas.types.Operation.prompt

Notice stairs
-------------

.. condition:: DRAMA.history[0].name do_look
.. condition:: PLAYER.state tas.types.Location.hall

[DRAMA]_

    |PLAYER_NAME| is in the |PLAYER_LOCN|.
    She stands at the foot of some **stairs**. Behind is her **bedroom**.
    Ahead the **kitchen**.

    Looking around, she is aware of:

{0}

.. property:: DRAMA.state tas.types.Operation.prompt

Inspect
-------

.. condition:: DRAMA.history[0].name do_inspect

[DRAMA]_

    |INPUT_TEXT|

{0}

.. property:: DRAMA.state tas.types.Operation.prompt

Look
----

.. condition:: DRAMA.history[0].name do_look

[DRAMA]_

    |PLAYER_NAME| is in the |PLAYER_LOCN|.
    Looking around, she is aware of:

{0}

.. property:: DRAMA.state tas.types.Operation.prompt

.. |INPUT_TEXT| property:: DRAMA.input_text
.. |PLAYER_NAME| property:: PLAYER.name
.. |PLAYER_LOCN| property:: PLAYER.location.title
