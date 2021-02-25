.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-01-10
:project:   Tea and Sympathy
:version:   |VERSION|
:dwell:     0
:pause:     0

.. entity:: PLAYER
   :types:  tas.types.Character
   :states: tas.tea.Motivation.player

.. entity:: NPC
   :types:  tas.types.Character
   :states: tas.tea.Motivation.paused

.. entity:: DRAMA
   :types:  tas.sympathy.TeaAndSympathy

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Paused
======

{0}

.. property:: DRAMA.prompt ?
.. property:: NPC.state tas.tea.Motivation.acting
.. property:: SETTINGS.catchphrase-colour-gravity hsl(209.33, 96.92%, 12.75%)
