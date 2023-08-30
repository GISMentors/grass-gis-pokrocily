Import lidarových dat
=====================

Před importem dat je potřeba vytvořit příslušnou lokaci, viz kapitola
:skoleni:`struktura dat
<grass-gis-zacatecnik/intro/struktura-dat.html>` a :skoleni:`tvorba
lokace <grass-gis-zacatecnik/data/tvorba-lokace.html>` ze školení
:skoleni:`GRASS GIS pro začátečníky <grass-gis-zacatecnik>`. Lokaci
pro import dat v textovém či binárním formátu lidarových dat vytvoříme
typicky :skoleni:`na základě EPSG kódu
<grass-gis-zacatecnik/data/tvorba-lokace.html#lokace-sjtsk>`.

..
    U binarního formátu LAS/LAZ je možné, vzhledem k tomu, že tento
    formát obvykle obsahuje tuto informaci (i když to není nutně
    pravidlem), vytvořit lokaci :skoleni:`na základě vstupního souboru
    <grass-gis-zacatecnik/data/tvorba-lokace.html#lokace-srtm>`.

Obecně řečeno lze vstupní lidarová data importovat do systému GRASS
jako :skoleni:`vektorová <grass-gis-zacatecnik/intro/vektor.html>`
nebo :skoleni:`rastrová <grass-gis-zacatecnik/intro/rastr.html>`
data. V případě importu lidarových dat do rastrové reprezentace hraje
zásadní roli :skoleni:`výpočetní region
<grass-gis-zacatecnik/_build/html/intro/region.html>`.

Textový formát XYZ
------------------

Vstupní soubor obsahuje souřadnice *x,y,z* pro každý bod na jednom
řádku. Souřadnice jsou odděleny většinou bílým znakem jako je mezera
nebo tabulátor. Pro vytvoření rastrového výstupu lze použít modul
:grasscmd:`r.in.xyz`, resp. :grasscmd:`v.in.ascii` v případě výstupu
vektorového. Druhý uvedený modul importuje bodová data tak, jak jsou
uvedena na vstupu. Modul :grasscmd:`r.in.xyz` se chová odlišně,
vytvoří na základě agregace načtených bodů do rastrových buněk
aktuálního výpočetního regionu dle zvolené statistické metody
(parametr :option:`method`, výchozí je průměrná hodnota - *mean*)
novou rastrovou mapu.

.. _lidar-xyz-raster:

Rastrová reprezentace
^^^^^^^^^^^^^^^^^^^^^

Příklad importu si ukážeme na souboru *HLIN04_5g.xyz* z kapitoly
:doc:`dmr-dmp-cuzk`.

::
   
   -625002.344 -1089749.632 502.825
   -625000.53 -1089735.192 502.585
   -625006.071 -1089779.418 504.849
   ...
   
.. note:: V tomto případě jsou data v souřadnicovém systému S-JTSK
          (:epsg:`5514`).

Modul :grasscmd:`r.in.xyz` vzhledem k tomu, že provádí agregaci
načtených dat, se na rozdíl od ostatních importních modulů řídí
aktuálním výpočetním regionem. Proto je třeba před importem nastavit
na základě vstupních dat výpočetní region. K tomu nám poslouží
přepínače :option:`-sg`.

.. _lidar-import-scan:

.. code-block:: bash

   r.in.xyz -sg input=HLIN04_5g.xyz separator=space
                
   n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334

.. note:: Ve verzi GRASS GIS 7.2.0 a nižší je třeba ještě zadat
          parametr :option:`output`, a to i přestože modul žádný výstup
          v tomto případě nevytváří.
      
Výsledek nám poslouží pro nastavení rozsahu výpočetního regionu pomocí
:grasscmd:`g.region`, na nás bude zvolit vhodné prostorové
rozlišení. V našem případě zvolíme 1 metr.

.. code-block:: bash

   g.region n=-1088000.076 s=-1090000.059 e=-624999.829 w=-627499.828 b=461.312 t=554.334 res=1

.. note:: Přepínačem :option:`-p` můžeme vytisknout pro kontrolu
   aktuální nastavení.

   .. code-block:: bash

      g.region -p

   ::

      north:      -1088000.076
      south:      -1090000.059
      west:       -627499.828
      east:       -624999.829
      nsres:      0.9999915
      ewres:      0.9999996

   .. _lidar-import-align:

   Modul :grasscmd:`g.region` provádí zarovnání na hraniční
   souřadnice, proto prostorové rozlišení neodpovídá přesně zadané
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

   .. _region_cell_center:

   Další možností je nastavit region tak, aby vstupní body padly do
   centra rastrových buněk. V tomto případě rozšíříme rozsah regionu o
   polovinu nastaveného prostorového rozlišení, v našem případě tedy o
   0,5 metru.

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

Poté již provedeme import (vynecháme přepínače :option:`-sg` a přidáme
parametr :option:`output`):

.. code-block:: bash
                
   r.in.xyz input=HLIN04_5g.xyz separator=space output=HLIN04_5g

.. _lidar-import-xyz-vektor:

Vektorová reprezentace
^^^^^^^^^^^^^^^^^^^^^^
   
Pokud chceme vstupní data importovat jako bodovou vektorovou mapu,
použijeme modul :grasscmd:`v.in.ascii`. V tomto případě se data
naimportují v původní podobě, nedochází k žádné formě agregace tak
jako u :grasscmd:`r.in.xyz`.

.. code-block:: bash

   v.in.ascii input=HLIN04_5g.xyz output=HLIN04_5g separator=space z=3 -tbz

.. important:: Import lze urychlit přepínačem :option:`-t` (nevytvářet
          atributovou tabulku) a :option:`-b` (nesestavovat
          topologii).

          Ve výchozím nastavení modul importuje body jako 2D. Pomocí
          přepínače :option:`-z` si vynutíme výstup do 3D vektorové
          mapy. Index sloupce se z-tovou souřadnici definujeme pomocí
          parametru :option:`z`.

.. figure:: images/import-rast-vect.png

   Ilustrace importu lidarových dat do rastrové a vektorové bodové mapy.
   
Binární formát LAS/LAZ
----------------------

Data v binárním formátu `LAS
<https://www.asprs.org/committee-general/laser-las-file-format-exchange-activities.html>`__
či komprimované formě LAZ lze do systému GRASS naimportovat podobně
jako data v textovém formátu, a to jako rastrovou mapu
(:grasscmd:`r.in.lidar`) anebo jako mapu vektorovou
(:grasscmd:`v.in.lidar`).

.. _lidar-las-raster:

Rastrová reprezentace
^^^^^^^^^^^^^^^^^^^^^

Modul :grasscmd:`r.in.lidar` podobně jako :grasscmd:`r.in.xyz` (viz
:ref:`Textový formát XYZ <lidar-xyz-raster>`) provádí agregaci
vstupních bodů v aktuálním výpočetním regionu, a to na základě zvolené
statistické metody (parametr :option:`method`, výchozí metoda je
průměrná hodnota *mean*).

Na rozdíl od výše zmíněného modulu umožňuje :grasscmd:`r.in.lidar`
nastavit výpočetní region pro import automaticky na základě vstupních
dat. K tomu slouží přepínač :option:`-e`. V tomto ohledu se hodí
použít ještě přepínač :option:`-n`, který nastaví po importu výpočetní
region na základě vstupních dat. Prostorové rozlišení regionu
nastavíme parametrem :option:`resolution`.
   
.. code-block:: bash

   r.in.lidar input=pf_VIMP27_g.laz output=pf_VIMP27_g resolution=1 -ne

.. important:: V případě, že vstupní soubor neobsahuje informace o
   souřadnicovém připojení, tak příkaz skončí chybou:

   ::
      
      ERROR: Projection of dataset does not appear to match current location.

      GRASS LOCATION PROJ_INFO is:
      name: S-JTSK / Krovak East North
      datum: S_JTSK
      ellps: bessel
      proj: krovak
      lat_0: 49.5
      lon_0: 24.83333333333333
      alpha: 30.28813972222222
      k: 0.9999
      x_0: 0
      y_0: 0
      no_defs: defined
      towgs84: 570.8,85.7,462.8,4.998,1.587,5.261,3.56

      Import dataset PROJ_INFO is:
      Dataset proj = 0 (unreferenced/unknown)

      In case of no significant differences in the projection definitions,
      use the -o flag to ignore them and use current location definition.
      Consider generating a new location with 'location' parameter from
      input data set.

   V tomto případě, pokud jste si jisti, že vstupní data jsou
   lokalizována v souřadnicovém systému aktuální GRASS lokace,
   přidejte přepínač :option:`-o`, který kontrolu souřadnicového
   systému přeskočí.

   .. tip:: Rozsah souřadnic vstupních dat lze zjistit pomocí
      přepínače :option:`-p`.

      .. code-block:: bash
                      
         r.in.lidar input=pf_VIMP27_g.laz -p

      ::

         Using LAS Library Version 'libLAS 1.8.1 with GeoTIFF 1.4.2 LASzip 2.0.1'
         ...
         Number of Point Records:           4997968
         ...
         Min X Y Z:                         -807500 -1.156e+06 804.294
         Max X Y Z:                         -805000 -1.154e+06 1061.49
         ...

      Z výše uvedeného je zřejmé, že jsou vstupní data v souřadnicovém
      systému S-JTSK :epsg:`5514`.

.. _lidar-las-raster-steps:
   
.. note:: Pokud si přejete větší kontrolu nad procesem importu, tak
   lze podobně jako v případě importu :ref:`textových dat
   <lidar-xyz-raster>` rozložit proces do dvou kroků. Nejprve určit
   nastavení výpočetního regionu na základě vstupních dat a poté
   provést samotný import.

   .. code-block:: bash

      r.in.lidar input=pf_VIMP27_g.laz -sgo

   Výsledek, v našem případě

   ::
   
      n=-1154000.000000 s=-1155999.999000 e=-805000.000000 w=-807499.998000 b=804.294000 t=1061.487000


   použijeme pro nastavení výpočetního regionu včetně požadovaného
   rozlišení (parametr :option:`res`). Nezapomene na přepínač
   :option:`-a`, který zarovná nastavení právě podle hodnoty
   prostorového rozlišení.

   .. code-block:: bash
                     
      g.region n=-1154000.000 s=-1155999.999 e=-805000.000 w=-807499.998 b=804.294 t=1061.487 res=1 -a

   Poté již provedeme import:

   .. code-block:: bash

      r.in.lidar input=pf_VIMP27_g.laz output=pf_VIMP27_g -o

Základní metadata importované rastrové mapy vypíšeme pomocí modulu
:grasscmd:`r.info`.

.. code-block:: bash

   r.info map=pf_VIMP27_g

::
   
   |   Rows:         2000                                                       |
   |   Columns:      2500                                                       |
   |   Total Cells:  5000000                                                    |
   ...
   |            N:   -1154000    S:   -1156000   Res:     1                     |
   |            E:    -805000    W:    -807500   Res:     1                     |
   |   Range of data:    min = 804.313  max = 1061.487                          |
   ...
   
.. _lidar-import-las-vektor:

Vektorová reprezentace
^^^^^^^^^^^^^^^^^^^^^^

Pro vytvoření vektorové mapy na základě vstupních dat slouží modul
:grasscmd:`v.in.lidar`.

.. code-block:: bash

   v.in.lidar input=pf_VIMP27_g.laz output=pf_VIMP27_g

.. important:: Podobně jako v případě importu :ref:`textových dat
   <lidar-import-xyz-vektor>` lze proces urychlit tím, že nebudeme
   vytvářet atributová data (pokud je nepotřebujeme, např. v případě
   již klasifikovaných dat určených pro tvorbu digitálního modelu
   terénu, viz kapitola :doc:`dmr-dmp-cuzk`) a současně přeskočíme
   tvorbu topologie, která u bodových dat stejně nedává smysl. V našem
   případě ještě použijeme přepínač :option:`-o`, který přeskočí
   kontrolu souřadnicového systému.

   .. code-block:: bash

      v.in.lidar input=pf_VIMP27_g.laz output=pf_VIMP27_g  -otb

.. figure:: images/import-rast-vect-holes.png

   Ilustrace importu lidarových dat do rastrové a vektorové bodové
   mapy. V rastrové mapě jsou zřetelná místa bez vstupních bodových
   dat (no-data).

Základní metadata můžeme vypsat pomocí modulu :grasscmd:`v.info`.

.. code-block:: bash

   v.info map=pf_VIMP27_g

::

   |   Number of points:       4997968         Number of centroids:  0          |
   ...
   |               N:          -1154000    S:      -1155999.999                 |
   |               E:           -805000    W:       -807499.998                 |
   |               B:           804.294    T:          1061.487                 |

.. _v-outlier:      

Hustotu importovaných bodů můžeme ověřit pomocí modulu
:grasscmd:`v.lidar.edgedetection`. Vzhledem k tomu, že tento modul používá pro
výpočet nastavení aktualního výpočetního region, je potřeba jej
nejprve nastavit pomocí :grasscmd:`g.region` (nastavení regionu může
trvat několik sekund neboť chybí u vstupních dat topologie a modul
musí rozsah souřadnic spočítat přímo z bodových dat).

.. code-block:: bash

   g.region vector=pf_VIMP27_g
   v.lidar.edgedetection -e input=pf_VIMP27_g

::

   Estimated point density: 0.9996
   Estimated mean distance between points: 1
   
   
