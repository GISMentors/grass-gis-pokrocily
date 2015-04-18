Python
======

Základní verze skriptu
----------------------

Začneme verzí skriptu *bez vstupní parametrů*, názvy vstupních a
výstupních rastrových map jsou uvedeny na řádcích :lcode:`9` a
:lcode:`10`, resp. :lcode:`12` a :lcode:`13`.

Na řádku :lcode:`3` importuje z knihovny :doc:`../pygrass/index` třídu
:class:`Module`, která nám umožní z prostředí jazyka Python spouštěn
moduly GRASS jako je :grasscmd:`g.mapsets` (viz řádek :lcode:`6`) a
další.

.. literalinclude:: ndvi-v1.py
   :language: python
   :linenos:
   :emphasize-lines: 3, 6, 9, 10, 12, 13

Poznámky k volání modulů
^^^^^^^^^^^^^^^^^^^^^^^^                     

Moduly systému GRASS se volají se stejnými parametry jako z příkazové
řádky. Například pro volání na řádku :lcode:`6`:

.. literalinclude:: ndvi-v1.py
   :language: python
   :lines: 6

by korespondující zápis pro příkazovou řádku vypadal následovně:

.. code-block:: bash

   g.mapsets mapset=landsat operation=add --quiet
           
Jednotlivé parametry modulu se zadávaní jako argumenty třídy
:class:`Module`. Vyjímkou jsou globální přepínače jako je
:option:`--quiet`, :option:`--overwrite` a další, ty se zadávají jako
parametr s hodnotou ``True``, v tomto případě tedy ``quiet=True``.

.. note:: **Zkracování názvů parametrů**

   Při volání modulů z příkazové řádky lze názvy parametrů libovolně
   zkracovat, pouze z tou podmínkou aby byly jednoznačné, ve výše
   uvedeném případě bude následnující volání v pořádku i když méně
   čitelné.

   .. code-block:: bash

      g.mapsets landsat o=add --q

   Podobné zkracování názvů parametrů **není** při použití třídy
   :class:`Module` z knihovny :doc:`../pygrass/index` možné.
   
   
Pokročilejší verze skriptu
--------------------------

.. literalinclude:: ndvi-v2.sh
   :language: bash
   :linenos:
