Import dat
==========

Před importem dat je potřeba vytvořit příslušnou lokaci, viz kapitola
:skoleni:`struktura dat
<grass-gis-zacatecnik/intro/struktura-dat.html>` a :skoleni:`tvorba
lokace <grass-gis-zacatecnik/data/tvorba-lokace.html>`. V případě
textového formátu, který neobsahuje informaci o souřadnicovém systému,
vytvoříme typicky lokaci :skoleni:`na základě EPSG kódu
<grass-gis-zacatecnik/data/tvorba-lokace.html#priklad-vytvoreni-lokace-pro-data-v-souradnicovem-systemu-s-jtsk>`. U
binarního formátu LAS/LAZ je možné, vzhledem k tomu, že tento formát
obvykle obsahuje informaci o souřadnicovém systému, vytvořit lokaci
:skoleni:`na základě vstupího souboru
<grass-gis-zacatecnik/data/tvorba-lokace.html#lokace-srtm>`.

Textový formát XYZ
------------------

Data v textovém formátu XYZ umožňuje modul
:grasscmd:`r.in.xyz`. Vstupní soubor obsahuje souřadnice x,y,z pro
každý bod na jednom řádku. Souřadnice jsou odděleny většinou bílým
znakem jako je mezera nebo tabulátor.

Příklad importu si ukážeme na soubor *HLIN04_5g.xyz* z kapitoly
:doc:`dmr-dmp-cuzk`.

::
   
   -625002.344 -1089749.632 502.825
   -625000.53 -1089735.192 502.585
   -625006.071 -1089779.418 504.849
   ...
   
.. note:: V tomto případě jsou data v součadnicovém systému S-JTSK
          (:epsg:`5514`).

.. block-code:: bash

   r.in.xyz

.. note:: Ve verzích GRASS nižších než 7.2.1 je nutné nejprve zjistit
   výstupní region dat, nastavit jej jako výpočetní a teprve
   poté data importovat.

   .. code-block:: bash

      r.in.xyz -sg input=HLIN04_5g.xyz separator=space output=HLIN04_5g --o
      
      n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334

      # výstup použijeme pro nastavení aktuálního výpočetního regionu
      g.region n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334

      # poté již provedeme import (tj. vynecháme přepínače -sg)
      r.in.xyz input=HLIN04_5g.xyz separator=space output=HLIN04_5g
      ...
      r.in.xyz complete. 551013 points found in region.

Binární formát LAS/LAZ
----------------------
