2. Priemerná dlhodobá strata pôdy
=================================

Teoretické východiská
---------------------

Pri výpočtoch priemernej dlhodobej straty pôdy sa proces vodnej erózie
popisuje pomocou matematického modelu USLE, tzv. univerzálnej rovnice
straty pôdy:

.. _vzorec-G:

.. math::
   
   G = R \times K \times L \times S \times C \times P

Základné symboly:

 * G ... priemerná dlhodobá strata pôdy (:math:`t.ha^{-1} . rok^{-1}`)
 * R ... faktor eróznej účinnosti dažďa (:math:`MJ.ha^{-1} .cm.h^{-1}`)
 * K ... faktor erodovateľnosti pôdy (:math:`t.h.MJ^{-1} .cm^{-1} .rok^{-1}`) 
 * L ... faktor dĺžky svahu ( )
 * S ... faktor sklonu svahu ( ) 
 * C ... faktor ochranného vplyvu vegetačného krytu ( )
 * P ... faktor účinnosti protieróznych opatrení ( )

Vstupné dáta
------------

 * :map:`DMT` v rozlišení 10 x 10 m
 * :map:`HPJ` - hlavné pôdne jednotky (atribút :dbcolumn:`K_value`)
 * :map:`KPP` - komplexný prieskum pôd (atribút :dbcolumn:`K_faktor`)
 * :dbtable:`HPJ_K.xls`, :dbtable:`KPP_K.xls`, :dbtable:`LU_C.xls` - tabuľky s kódmi K a C
 * :map:`hpj_kpp_land` - zjednotenie HPJ a KPP a ich prienik s LU(atribút :dbcolumn:`a_b_K_faktor`)
 * :map:`A07_Povodi_IV` - povodia IV. rádu
 * :map:`maska.pack` - vrstva líniových a plošných prvkov prerušujúcich odtok
   
Postup
------

Na :num:`#schema-usle` je prehľadne znázornený navrhovaný postup. 

    .. _schema-usle:

    .. figure:: images/schema_b.png

        Grafická schéma postupu 

Z digitálneho modelu terénu (DMT) vytvoríme rastrovú mapu znázorňujúcu
sklonové pomery v stupňoch (*slope*). Tá bude potrebná neskôr na
výpočet :ref:`topografického faktora LS <ls-faktor>`. V prvom kroku
nastavíme :skoleni:`výpočtový región
<grass-gis-zacatecnik/intro/region.html>` na základe vstupného DMT a
následne použijeme modul :grasscmd:`r.slope.aspect`, viď.
:skoleni:`topografické analýzy
<grass-gis-zacatecnik/raster/analyzy-povrchu.html>`.

.. code-block:: bash
                
   g.region raster=dmt
   r.slope.aspect elevation=dmt slope=svah

.. figure:: images/1b.png
   :class: middle

   Hypsografické stupne (DMT) v metroch a sklonové pomery v stupňoch

Ďalej vytvoríme vyhladený DMT (:option:`filled`), rastrovú mapu smeru
odtoku do susednej bunky s najväčším sklonom (:option:`direction`) a
rastrovú mapu znázorňujúcu akumuláciu toku v každej bunke
(:option:`accumulation`).

.. note:: Na vytvorenie vyhladeného DMT možno alternatívne použiť aj
          Addons modul :grasscmdaddons:`r.hydrodem`, pre výpočet smeru
          odtoku modul :grasscmd:`r.fill.dir` a pre akumuláciu odtoku
          :grasscmd:`r.watershed`.
          
Pred výpočtom si nastavíme masku podľa záujmového územia pomocou
modulu :grasscmd:`r.mask`.

.. code-block:: bash

   r.mask raster=dmt
   r.terraflow elevation=dmt filled=dmt_fill direction=dir swatershed=sink accumulation=accu tci=tci

.. figure:: images/2b.png
   :class: large

   Smer v stupňoch a akumulácia odtoku v :math:`m^2` vytvorené modulom :grasscmd:`r.terraflow`

.. _ls-faktor:
   
LS faktor
^^^^^^^^^

LS faktor (topografický faktor) možno vypočítať podľa vzťahu:

.. math::
   
   LS = (accu \times \frac{10.0}{22.13})^{0.6} \times (\frac{sin(slope \times \frac{pi}{180})}{0.09})^{1.3}
   
Pre tieto účely využijeme nástroj :grasscmd:`r.mapcalc` ako hlavný
nástroj :skoleni:`mapovej algebry
<grass-gis-zacatecnik/raster/rastrova-algebra.html>` v systéme GRASS.

V zápise pre tento nástroj bude rovnica vyzerať nasledovne:

.. code-block:: bash

   r.mapcalc expr="ls = pow(accu * (10.0 / 22.13), 0.6) * pow(sin(svah * (3.1415926/180)) / 0.09, 1.3)"

Nastavíme vhodnú tabuľku farieb:

.. code-block:: bash

   r.colors map=ls color=colors.txt

::
      
    0.00 128:64:64
    0.01 255:128:64
    0.05 0:255:0
    0.10 0:128:128
    0.20 0:128:255
    
.. figure:: images/3b.png
   :class: small

   Topografický faktor LS zahrňujúci vplyv dĺžky a sklonu svahu
   
K a C faktor
^^^^^^^^^^^^

Do aktuálneho mapsetu importujeme vektorovú vrstvu :map:`hpj_kpp_land`
(viď. :ref:`návod <hydrsk>` na jej vytvorenie).

.. tip:: V prípade, že mapa :map:`hpj_kpp_land` je len v inom mapsete,
         možno ju do aktuálneho mapsetu prekopírovať pomocou
         :grasscmd:`g.mapset`, tak, že najprv zmeníme mapset, pridáme
         mapu a potom sa vrátime do aktuálneho mapsetu. V správcovi
         vrstiev zvolíme pravým tlačidlom myši *Make a copy in the
         current mapset*.

Do jej atribútovej tabuľky pridáme dva nové stĺpce :dbcolumn:`K` a
:dbcolumn:`C`. To vykonáme pomocou :skoleni:`správcu atribútových dát
<grass-gis-zacatecnik/vector/atributy.html>` alebo modulu
:grasscmd:`v.db.addcolumn`.

.. code-block:: bash
                
   v.db.addcolumn map=hpj_kpp_land columns="K double"
   v.db.addcolumn map=hpj_kpp_land columns="C double" 

Hodnotu K faktora pre jednotlivé elementárne plochy priradíme pomocou
tabuľky :dbtable:`HPJ_K.xls`. Pre plochy bez hodnoty K faktora
doplníme údaje na základe pôdnych typov a subtypov podľa komplexného
prieskumu pôd (tabuľka :dbtable:`KPP_K.xls`). Hodnotu C faktora
poľnohospodársky využívaných oblastí zistíme z priemerných hodnôt pre
jednotlivé plodiny z tabuľky :dbtable:`LU_C.xls`. Na spájanie tabuliek
použijeme modul :grasscmd:`v.db.join`

Prevodové tabuľky je potrebné najprv naimportovať do prostredia GRASS
GIS. Použijeme modul :grasscmd:`db.in.ogr`:

.. code-block:: bash
                
   db.in.ogr in=KPP_K.xls out=kpp_k
   db.in.ogr in=HPJ_K.xls out=hpj_k
   db.in.ogr in=LU_C.xls out=lu_c
 
Potom pristúpime k pripojeniu tabuľky :dbtable:`hpj_k` k atribútom
vektorovej vrstvy :map:`hpj_kpp_land`, pričom spojítkom bude atribút
:dbcolumn:`HPJ_key`.

.. code-block:: bash 
            
   v.db.join map=hpj_kpp_land column=a_HPJ_key other_table=hpj_k other_column=HPJ 


Chýbajúce informácie o hodnote faktora ``K`` doplníme z tabuľky
:dbtable:`kpp_k` SQL dotazom prostredníctvom modulu
:grasscmd:`db.execute`.

.. code-block:: bash
   
   db.execute sql="UPDATE hpj_kpp_land SET K = (
   SELECT b.K FROM hpj_kpp_land AS a JOIN kpp_k as b ON a.a_b_KPP = b.KPP)
   WHERE K IS NULL"

V dalšom kroku doplníme hodnoty ``C`` faktora z importovanej tabuľky
:dbtable:`lu_c`.

.. code-block:: bash
                
   v.db.join map=hpj_kpp_land column=b_LandUse other_table=lu_c other_column=LU 

Údaje v atribútovej tabuľke si skontrolujeme, či sú vyplnené
správne. Použijeme SQL dotaz :grasscmd:`db.select`, pričom vyberieme
len prvé 3 záznamy.

.. code-block:: bash

   db.select sql="select cat,K,C from hpj_kpp_land where cat <= 5"

Výsledok môže vyzerať napríklad aj takto:

.. code-block:: bash

   cat|K|C
   1|0.13|0.19
   2|0.13|0.19
   3|0.13|0.19
   ...

Ďalej do atribútovej tabuľky pridáme nový atribút :dbcolumn:`KC`, do
ktorého uložíme súčin faktorov ``K * C``. To môžeme vykonať pomocou
:skoleni:`správcu atribútových dát
<grass-gis-zacatecnik/vector/atributy.html>` alebo modulom
:grasscmd:`v.db.addcolumn` v kombinácii s :grasscmd:`v.db.update`.

.. code-block:: bash

   v.db.addcolumn map=hpj_kpp_land columns="KC double"
   v.db.update map=hpj_kpp_land column=KC value="K * C"

Ukážkový výsledok pre prvé tri záznamy opäť skontrolujeme.

.. code-block:: bash

   db.select sql="select cat,K,C,KC from hpj_kpp_land where cat <= 3"

.. code-block:: bash

   cat|K|C|KC
   1|0.13|0.19|0.0247
   2|0.13|0.19|0.0247
   3|0.13|0.19|0.0247
   ...

V ďalšom kroku vektorovú mapu prevedieme na rastrovú reprezentáciu
modulom :grasscmd:`v.to.rast`. Pre zachovanie informácie použijeme
priestorové rozlíšenie *1 m* (:grasscmd:`g.region`,
viď. :skoleni:`výpočtový región
<grass-gis-zacatecnik/intro/region.html>`).

Pomocou modulu :grasscmd:`r.resamp.stats` potom vykonáme
prevzorkovanie na priestorové rozlíšenie DMT *10 m* a to na základe
priemeru hodnôt vypočítaného z hodnôt okolitých buniek. Týmto postupom
zabránime strate informácií, ku ktorému by došlo pri priamom prevode
na raster s rozlíšením *10 m*. Pri rasterizácii sa totiž hodnota bunky
rastra volí na základe polygónu, ktorý prechádza stredom bunky alebo
na základe polygónu, ktorý zaberá najväčiu čásť plochy bunky.

.. code-block:: bash
   
   g.region raster=dmt res=1 
   v.to.rast input=hpj_kpp_land output=hpj_kpp_land_kc use=attr attribute_column=KC

   g.region raster=dmt
   r.resamp.stats input=hpj_kpp_land_kc output=hpj_kpp_land_kc10 

Na obrázku :num:`#porovkn` je znázornená časť záujmového územia, kde
možno vidieť rastrovú vrstvu :map:`hpj_kpp_land_kc` pred (vľavo dole)
a po použití modulu :grasscmd:`r.resamp`.

.. _porovkn:

.. figure:: images/10a.png
   
   Časť záujmového územia s faktorom *KC* pred a po prevzorkovaní
                      
Kvôli vizualizácii nastavíme vhodnú :skoleni:`tabuľku farieb
<grass-gis-zacatecnik/raster/tabulka-barev.html>` a kvôli prehľadnosti
mapu premenujeme na :map:`kc` modulom :grasscmd:`g.rename`. Výsledok
je na :num:`#kc`.

.. code-block:: bash
                
   r.colors map=hpj_kpp_land_kc10 color=wave
   g.rename raster=hpj_kpp_land_kc10,kc

.. _kc:

.. figure:: images/11.png
   :class: small

   Faktor *KC* zahrňujúci vplyv erodovateľnosti pôdy a vplyv ochranného vplyvu vegetačného krytu

R a P faktor
^^^^^^^^^^^^

Hodnoty týchto parametrov nebudeme odvádzať ako tie predchádzajúce. V
tomto prípade jednoducho použijeme priemernú hodnotu ``R`` a ``P``
faktora pre Českú republiku, t.j ``R = 40`` a ``P = 1``.

Výpočet priemernej dlhodobej straty pôdy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stratu pôdy `G` vypočítame modulom :grasscmd:`r.mapcalc`
(:num:`#rmapcalc`), pričom vychádzame zo vzťahu, ktorý bol uvedený v
:ref:`teoretickej časti školenia <vzorec-G>`.

.. _rmapcalc:

.. figure:: images/15.png
   :class: small

Pre výslednú vrstvu zvolíme primeranú farebnú škálu, pridáme legendu,
mierku a mapu zobrazíme (:num:`#map-g`)

.. code-block:: bash
                
   r.mapcalc expr="g = 40 ∗ ls ∗ kc ∗ 1"
   r.colors -n -e map=g color=corine

.. _map-g:

.. figure:: images/12.png
   :class: small

   Vrstva s hodnotami predstavujúcimi priemernú dlhodobú stratu pôdy G
   v jednotkách :math:`t.ha^{-1} . rok^{-1}`)

.. note:: Na :num:`#map-g` je maximálna hodnota v legende *1*. Je to
    len z dôvodu, aby bol výsledok prehľadný a korešpondoval s farbami
    v mape. V skutočnosti parameter ``G`` nadobúda hodnotu až *230*,
    no pri takomto rozsahu by bola stupnica v legende jednofarebná (v
    našom prípade červená).  Zmeniť rozsah intervalu v legende bolo
    možné nastavením parametra *range*, konkrétnejšie príkazom
    :code:`d.legend raster=g range=0,1`.

Priemerná hodnota straty pre povodie
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
   
Na určenie priemernej hodnoty a sumy straty pre každé čiastkové
povodie využijeme modul :grasscmd:`v.rast.stats`. Kľúčovou vrstvou je
vektorová mapa povodí :map:`A07_Povodi_IV`, kde nastavíme prefix
:item:`g_` pre novovytvorený stĺpec. Z toho potom modulom
:grasscmd:`v.db.univar` zobrazíme štatistiky priemerných hodnôt straty
pôdy.

.. code-block:: bash
                
   v.rast.stats map=A07_Povodi_IV raster=g column_prefix=g method=average
   v.db.univar map=A07_Povodi_IV column=g_average

.. note:: Vektorová vrstva povodí musí byť v aktuálnom mapsete. Ak
          napríklad pracujeme v inom mapsete, stačí ak ju pridáme z
          mapsetu :mapset:`PERMANENT` a následne v menu pravým
          kliknutím na mapu zvolíme :item:`Make a copy in the current
          mapset`.

Pre účely vizualizácie vektorovú vrstvu prevedieme na raster, pomocou
modulu :grasscmd:`r.colors` nastavíme vhodnú tabuľku farieb a výsledok
prezentujeme, viď. :num:`#g-average`.

.. code-block:: bash
   
   v.to.rast input=A07_Povodi_IV output=pov_avg_G use=attr attribute_column=g_average
   r.colors -e map=pov_avg_G color=bgyr

.. _g-average:

.. figure:: images/13.png

   Povodia s priemernými hodnotami straty pôdy

.. note:: Z dôvodu prehľadnosti je opäť interval v legende
          upravený. Maximálna hodnota priemernej straty pôdy na
          povodie je až *0.74* (v jednotkách :math:`t.ha^{-1}
          . rok^{-1}`)
    
Zahrnutie prvkov prerušujúcich odtok
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pre výpočet uvedený vyššie vychádza strata pôdy v niektorých miestach
enormne vysoká. To je spôsobené tým, že vo výpočtoch nie sú zahrnuté
líniové a plošné prvky prerušujúce povrchový odtok. Týmito prvkami sú
najmä budovy, priekopy diaľnic a ciest, železničné trate alebo múry
lemujúce pozemky.

Aby sme zistili presnejšie hodnoty, je nutné tieto prvky do výpočtu
zahrnúť. Pre tento účel použijeme masku líniových a plošných prvkov
prerušujúcich odtok :map:`maska.patch` a vypočítame nové hodnoty LS
faktora a straty pôdy. Vstupom bude :map:`dmt` bez prvkov
prerušujúcich odtok (:num:`#dmt-m`).

.. code-block:: bash
   
   r.unpack -o input= ... /MASK.pack output=mask
   r.mask raster=mask
   r.terraflow elevation=dmt filled=dmt_fill_m direction=dir_m swatershed=sink_m accumulation=accu_m tci=tci_m

.. _dmt-m:

.. figure:: images/14a.png
   :class: small

   Vrstva digitálneho modelu terénu vstupujúca do výpočtov bez prvkov prerušujúcich odtok


Ďalej dopočítame faktor LS a následne G.

.. code-block:: bash

   r.mapcalc expr="ls_m = pow(accu_m * (10.0 / 22.13), 0.6) * pow(sin(svah * (3.1415926/180)) / 0.09, 1.3)"
   r.mapcalc expr="g_m = 40 ∗ ls_m ∗ kc ∗ 1"
   
   r.colors map=ls_m color=wave
   r.colors -n -e map=g_m color=corine

V poslednom kroku vymažeme masku, výsledky zobrazíme a porovnáme
(:num:`#ls-porov` a :num:`#g-porov`).
             
.. _ls-porov:

.. figure:: images/ls_porov.png
   :scale: 55%
     
   Porovnanie hodnôt faktora LS bez ohľadu na prvky prerušujúce odtok
   (vľavo) a s prvkami prerušujúcimi odtok (vpravo)

.. _g-porov:

.. figure:: images/g_porov.png
   :scale: 57%

   Porovnanie výsledkov USLE bez ohľadu na prvky prerušujúce odtok
   (vľavo) a s prvkami prerušujúcimi odtok (vpravo)

Priemerná hodnota straty pre povodie s prvkami prerušujúcimi odtok
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Opäť využijeme modul :grasscmd:`v.rast.stats`. Vektorovej mape povodí
:map:`A07_Povodi_IV` nastavíme prefix :item:`g_m` pre novovytvorený
stĺpec a potom modulom :grasscmd:`v.db.univar` zobrazíme štatistiky
priemerných hodnôt straty pôdy. Výsledok v rastrovej podobe je na
:num:`#g-m-average`.

.. code-block:: bash
                
   v.rast.stats map=A07_Povodi_IV raster=g_m column_prefix=g_m method=average
   v.db.univar map=A07_Povodi_IV column=g_m_average
   
   v.to.rast input=A07_Povodi_IV output=pov_avg_G_m use=attr attribute_column=g_m_average
   r.colors -e map=pov_avg_G_m color=bgyr

.. _g-m-average:

.. figure:: images/16.png

   Povodia s priemernými hodnotami straty pôdy s uvážením prvkov,
   ktoré prerušujú odtok

Na záver urobíme rozdiely (modul :grasscmd:`r.mapcalc`) výsledných
vrstiev bez a s uvážením prvkov, ktoré prerušujú odtok pre faktor
*LS*, hodnoty predstavujúce priemernú dlhodobú stratu pôdy *G* a
povodia s priemernými hodnotami straty pôdy *G_pov*. Nazveme ich
:map:`delta_ls`, :map:`delta_g` a :map:`delta_pov_avg` a každej
nastavíme farbnú stupnicu :item:`differences`. Sú na :num:`#diff`.

.. code-block:: bash

   r.mapcalc expression=delta_ls = ls - ls_m
   r.mapcalc expression=delta_g = g - g_m
   r.mapcalc expression=delta_pov_avg = pov_avg_G - pov_avg_G_m

   r.colors map=delta_ls color=differences
   r.colors map=delta_g color=differences
   r.colors map=delta_pov_avg color=differences

.. _diff:

.. figure:: images/diff.png
   :scale: 55%

   Znázornenie rozdielov rastrových vrstiev LS, G a G_pov, ktoré
   vznikli bez uváženia a s uvážením prvkov, ktoré prerušujú odtok
 
Poznámky
--------

GRASS ponúka na výpočet USLE dva užitočné moduly :grasscmd:`r.uslek` a
:grasscmd:`r.usler`.
