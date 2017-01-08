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

Obecně řečeno lze vstupní Lidarová data importovat do systému GRASS
jako vektorová a rastrová data.

Textový formát XYZ
------------------

Data v textovém formátu XYZ umožňuje modul
:grasscmd:`r.in.xyz`. Vstupní soubor obsahuje souřadnice x,y,z pro
každý bod na jednom řádku. Souřadnice jsou odděleny většinou bílým
znakem jako je mezera nebo tabulátor. Modul vytvoří na základě
agregace načtených bodů do rastrových buněk dle zvolené statistické
metody (parametr :option:`method`, výchozí je průměrná hodnota -
*mean*) novou rastrovou mapu.

Příklad importu si ukážeme na soubor *HLIN04_5g.xyz* z kapitoly
:doc:`dmr-dmp-cuzk`.

::
   
   -625002.344 -1089749.632 502.825
   -625000.53 -1089735.192 502.585
   -625006.071 -1089779.418 504.849
   ...
   
.. note:: V tomto případě jsou data v součadnicovém systému S-JTSK
          (:epsg:`5514`).

Modul :grasscmd:`r.in.xyz` vzhledem k tomu, že provádí agregaci
načtených dat, se na rozdíl od ostatních importních modulů řídí
aktuálním výpočetním regionem. Proto je třeba před importem nastavit
výpočetní region na základě vstupních dat. K tomu nám poslouží
přepínače :option:`-sg`.

.. code-block:: bash

   r.in.xyz -sg input=HLIN04_5g.xyz separator=space output=HLIN04_5g --o
                
   n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334

Výsledek nám poslouží pro nastavení rozsahu výpočetního regionu, na
nás bude zvolit vhodné prostorové rozlišení. V našem případě zvolíme 1
metr.

.. code-block:: bash

   g.region n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334 res=1 -p

.. note:: Přepínač :option:`-p` můžeme vytiskout pro kontorolu výsledek.

   ::

      north:      -1088000.076
      south:      -1090000.059
      west:       -627499.828
      east:       -624999.829
      nsres:      0.9999915
      ewres:      0.9999996

   Module :grasscmd:`g.region` ve výchozím nastavení provádí zarovnání
   na rozsah, proto není prostorové rozlišení přesně rovno zadané
   hodnotě. Zarovnání regionu na rozlišení můžeme vynutit pomocí
   přepínače :option:`-a`.

   .. code-block:: bash

      g.region n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334 res=1 -pa

   ::
      
      north:      -1088000
      south:      -1090001
      west:       -627500
      east:       -624999
      nsres:      1
      ewres:      1

   Další možností je nastavit region tak, aby vstupní body po okrajích
   padly do centra rastrových buněk. V tomto případě rozšíříme rozsah
   regionu o polovinu nastaveného prostorového rozlišení, v našem
   případě tedy 0,5 metru.

   .. code-block:: bash

      g.region n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334
      g.region n=n+0.5 s=s-0.5 w=w-0.5 e=e+0.5 res=1 -p

   ::

      north:      -1087999.576
      south:      -1090000.559
      west:       -627500.328
      east:       -624999.329
      nsres:      0.9999915
      ewres:      0.9999996

Poté již provedeme import (tj. vynecháme přepínače :option:`-sg`):

.. code-block:: bash
                
   r.in.xyz input=HLIN04_5g.xyz separator=space output=HLIN04_5g

Pokud chceme vstupní data importovat jako vektorovou mapu, použijeme
modul :grasscmd:`v.in.ascii`.

.. note:: Import lze urychlit přepínačem :option:`-t` (nevytvářet
          atributovou tabulku) a :option:`-b` (nesestavovat
          topologii).

          Ve výchozím nastavení modul importuje body jako 2D. Pomocí
          přepínače :option:`-z` si vynutíme výstup do 3D vektorové
          mapy. Index sloupce se z-tovou souřadnici definujeme pomocí
          parametru :option:`z`.

.. code-block:: bash

   v.in.ascii in=HLIN04_5g.xyz out=HLIN04_5g separator=space z=3 -tbz

Binární formát LAS/LAZ
----------------------
