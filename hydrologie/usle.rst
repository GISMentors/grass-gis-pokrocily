Průměrná dlouhodobá ztráta půdy
===============================

Teoretické základy
------------------

Průměrnou roční ztrátu půdy způsobenou odtokem z pozemku určitého
sklonu a způsobu využívaní je možno predikovat pomocí matematického
modelu :wikipedia:`USLE <Univerzální rovnice ztráty půdy>`,
tzv. *univerzální rovnice ztráty půdy*:

.. _vzorec-G:

.. math::
   
   G = R \times K \times L \times S \times C \times P

kde:

 * G - průmerná dlouhodobá ztráta půdy (:math:`t.ha^{-1} . rok^{-1}`)
 * R - faktor erozní účinnosti deště (:math:`MJ.ha^{-1} .cm.h^{-1}`)
 * K - faktor eroze půdy (:math:`t.h.MJ^{-1} .cm^{-1} .rok^{-1}`) 
 * L - faktor délky svahu (:math:`-`)
 * S - faktor sklonu svahu (:math:`-`)
 * C - faktor ochranného vlivu vegetačního krytu (:math:`-`) 
 * P - faktor účinnosti protierozních opatření (:math:`-`) 
          
Vstupní data
------------

 * :map:`hpj.shp` - vektorová vrstva hlavních půdních jednotek z kódů BPEJ
 * :map:`kpp.shp` - vektorová vrstva komplexního průzkumu půd
 * :map:`landuse.shp` - vektorová vrstva využití území
 * :map:`povodi.shp` - vektorová vrstva povodí IV. řádu s návrhovými
   srážkami :math:`H_s` (doba opakovaní 2, 5, 10, 20, 50 a 100 let)
 * :dbtable:`hpj_k.csv` - číselník s kódem `K` pro hlavní půdní jednotky, :numref:`ciselniky` vlevo
 * :dbtable:`kpp_k.csv` - číselník s kódem `K` pro vrstvu komplexního
   průzkumu půd, :numref:`ciselniky` vpravo
 * :dbtable:`lu_c.csv` - číselník s kódem `C` pro vrstvu využití území,
   :numref:`ciselniky` vpravo
 * :map:`dmt.tif` - digitální model terénu v rozlišení 10 x 10 m,
   :numref:`dmt-maska` vlevo
 * :map:`maska.pack` - oblast území bez liniových a plošných prvků
   prerušujících odtok, :numref:`dmt-maska` vpravo
             
Navrhovaný postup
-----------------

:ref:`1.<krok1>` 
sjednocení vrstvy hlavních půdních jednotek a komplexního průzkumu půd

:ref:`2.<krok2>` 
připojení hodnot faktoru `K` k elementárním plochám

:ref:`3.<krok3>` 
průnik vrstvy elementárních ploch a využití území

:ref:`4.<krok4>` 
připojení hodnot faktoru `C`

:ref:`5.<krok5>` 
výpočet parametru `KC` 

:ref:`6.<krok6>` 
vytvoření rastrové mapy sklonu a akumulace odtoku v každé buňce

:ref:`7.<krok7>` 
výpočet parametru `LS`

:ref:`8.<krok8>` výpočet `G` a vytvoření rastru s hodnotami
představující průměrnou dlouhodobou ztrátu půdy

:ref:`9.<krok9>` 
výpočet průměrných hodnot `G` pro povodí

:ref:`10.<krok10>` 
vytvoření rastrových vrstev `LS` a `G` s maskou

:ref:`11.<krok11>` 
výpočet průměrných hodnot `G` pro povodí s maskou 

.. _schema-usle:

.. figure:: images/schema_usle.png
   :class: large

   Grafické schéma postupu. 

Znázornění vstupních vektorových dat spolu s atributovými tabulkami je
totožné se :ref:`vstupními vektorovými daty pro metodu SCS CN
<scs-cn-vstupni-data>`. Digitální model reliéfu a oblast řešeného
území bez liniových a plošných prvků přerušující odtok (maska) jsou
zobrazena na :numref:`dmt-maska`. Tabulky s faktory `K` a `C` jsou
uvedeny na :numref:`ciselniky`.

.. _dmt-maska:

.. figure:: images/dmt_maska.png
   :class: middle

   Vrstva digitálního modelu terénu a oblast řešeného území bez prvků 
   přerušujících odtok.

.. _ciselniky:

.. figure:: images/ciselniky_usle.png
   :class: middle

   Číselníky s hodnotami *K* a *C*. 

Postup zpracování v GRASS GIS
-----------------------------

Z digitálního modelu terénu (DMT) vytvoříme rastrovou mapu
znázorňující sklonové poměry ve stupních (*slope*). Ten bude potřebný
později pro výpočet :ref:`topografického faktoru LS <ls-faktor>`. V
prvním kroku nastavíme *výpočetní region* na základě vstupního DMT a
následně použijeme modul :grasscmd:`r.slope.aspect`.

.. tip:: Podrobné informace ohledně :skoleni:`výpočetního regionu
   <grass-gis-zacatecnik/intro/region.html>` a :skoleni:`topografických
   analýz <grass-gis-zacatecnik/rastrova_data/analyzy-povrchu.html>` ve
   školení GRASS GIS pro začátečníky.

.. code-block:: bash
                
   g.region raster=dmt
   r.slope.aspect elevation=dmt slope=svah

.. figure:: images/1b.png
   :class: middle

   Hypsografické stupně (DMT) v metrech a sklonové poměry v stupních.

Dále vytvoříme vyhlazený DMT (:option:`filled`), rastrovou mapu směru
odtoku do sousední buňky s největším sklonem (:option:`direction`) a
rastrovou mapu znázorňující akumulaci odtoku v každé buňce
(:option:`accumulation`).

.. note:: Pro vytvoření vyhlazeného DMT možno alternativně použít také
   Addons modul :grasscmdaddons:`r.hydrodem`, pro výpočet směru
   odtoku modul :grasscmd:`r.fill.dir` a pro akumulaci odtoku
   :grasscmd:`r.watershed`.

   .. todo:: Tady by chtělo hlubší analýzu, v čem se moduly liší, to
             je otázka na kolegy z k143.
   
Před výpočtem si nastavíme masku podle zájmového území pomocí
modulu :grasscmd:`r.mask`.

.. code-block:: bash

   r.mask raster=dmt
   r.terraflow elevation=dmt filled=dmt_fill direction=dir swatershed=sink accumulation=accu tci=tci

.. figure:: images/2b.png
   :class: large

   Směr odtoku ve stupních a akumulace odtoku v :math:`m^2` vytvořené modulem
   :grasscmd:`r.terraflow`.

.. _ls-faktor:
   
LS faktor
^^^^^^^^^

LS faktor (topografický faktor) možno vypočítat podle vztahu:

.. math::
   
   LS = 1.6 \times (accu \times \frac{res}{22.13})^{0.6} \times (\frac{sin(slope \times \frac{pi}{180})}{0.09})^{1.3}

kde:

* `accu` je rastrová mapa akumulace odtoku
* `res` je prostorové rozlišení DMT
* `slope` je rastrová mapa míry sklonu

.. note:: Rovnice vychází z `metody Mitášová
          <http://www4.ncsu.edu/~hmitaso/gmslab/denix/usle.html>`__.
            
Pro tyto účely využijeme nástroj :grasscmd:`r.mapcalc` jako hlavní
nástroj mapové algebry v systému GRASS.

.. tip:: Více na téma :skoleni:`mapové algebry
   <grass-gis-zacatecnik/rastrova_data/rastrova-algebra.html>` ve
   školení GRASS GIS pro začátečníky.
         
V zápisu pro tento nástroj bude rovnice vypadat následovně:

.. code-block:: bash

   r.mapcalc expr="ls = 1.6 * pow(accu * (10.0 / 22.13), 0.6) * pow(sin(svah * (3.1415926/180)) / 0.09, 1.3)"

.. note:: Nastavíme vhodnou tabulku barev:

   .. code-block:: bash

      r.colors map=ls color=colors.txt

   např.
   
   ::
      
    0.00 128:64:64
    0.01 255:128:64
    0.05 0:255:0
    0.10 0:128:128
    0.20 0:128:255
    
.. figure:: images/3b.png
   :class: small

   Topografický faktor LS zahrnující vliv délky a sklonu svahu.
   
K a C faktor
^^^^^^^^^^^^

Vytvoříme vektorovou vrstvu elementárních ploch :map:`hpj_kpp_land`
(viz. :ref:`návod <scs-cn-hpj_kpp_land>` na její vytvoření).

.. code-block:: bash

   v.overlay ainput=hpj binput=kpp operator=or output=hpj_kpp
   v.overlay ainput=hpj_kpp binput=landuse operator=and output=hpj_kpp_land

Do její atributové tabulky přidáme dva nové sloupce :dbcolumn:`K` a
:dbcolumn:`C`. To provedeme pomocí :skoleni:`správce atributových dat
<grass-gis-zacatecnik/vektorova_data/atributy.html>` anebo modulu
:grasscmd:`v.db.addcolumn`.

.. code-block:: bash
                
   v.db.addcolumn map=hpj_kpp_land columns="K double"
   v.db.addcolumn map=hpj_kpp_land columns="C double" 

Hodnotu K faktoru pro jednotlivé elementární plochy přiřadíme pomocí
číselníku :dbtable:`hpj_k.csv`. Pro plochy bez hodnoty K faktoru
doplníme údaje na základě půdních typů a subtypů podle komplexního
průzkumu půd (tabulka :dbtable:`kpp_k.csv`). Hodnota C faktoru
zemědělsky využívaných oblastí zjistíme z průměrných hodnot pro
jednotlivé plodiny z tabulky :dbtable:`lu_c.csv`. Na spojení tabulek
použijeme modul :grasscmd:`v.db.join`.

Převodové tabulky je potřebné nejprve naimportovat do prostředí GRASS
GIS. Použijeme modul :grasscmd:`db.in.ogr`:

.. code-block:: bash
                
   db.in.ogr in=kpp_k.csv out=kpp_k
   db.in.ogr in=hpj_k.csv out=hpj_k
   db.in.ogr in=lu_c.csv out=lu_c
 
Potom přistoupíme k připojení tabulky :dbtable:`hpj_k` k atributům
vektorové vrstvy :map:`hpj_kpp_land`, klíčem bude atribut
:dbcolumn:`HPJ`.

.. code-block:: bash 
            
   v.db.join map=hpj_kpp_land column=a_HPJ other_table=hpj_k other_column=HPJ 

Chýbějící informace hodnoty faktoru ``K`` doplníme z tabulky
:dbtable:`kpp_k` SQL dotazem prostřednictvím modulu
:grasscmd:`db.execute`.

.. code-block:: bash
   
   db.execute sql="UPDATE hpj_kpp_land SET K = (
   SELECT b.K FROM hpj_kpp_land AS a JOIN kpp_k as b ON a.a_b_KPP = b.KPP)
   WHERE K IS NULL"

V dalším kroku doplníme hodnoty ``C`` faktoru z importované tabulky
:dbtable:`lu_c`.

.. code-block:: bash
                
   v.db.join map=hpj_kpp_land column=b_LandUse other_table=lu_c other_column=LU 

Údaje v atributové tabulky si zkontrolujeme, zda jsou vyplněny
správně. Použijeme SQL dotaz :grasscmd:`db.select`, přitom vybere jen
první tři záznamy (resp. elementární plochy).

.. code-block:: bash

   db.select sql="select cat,K,C from hpj_kpp_land where cat <= 3"

Výsledek může vypadat například takto:

.. code-block:: bash

   cat|K|C
   1|0.13|0.19
   2|0.13|0.19
   3|0.13|0.19
   ...

.. note:: Atribut :dbcolumn:`cat` je hodnota, která propojuje
   geometrii prvků se záznamem v atributové tabulce.
             
Dále do atributové tabulky přidáme nový atribut :dbcolumn:`KC`, do
kterého uložíme součin faktorů ``K * C``. To můžeme vykonat pomocí
:skoleni:`správce atributových dat
<grass-gis-zacatecnik/vektorova_data/atributy.html>` anebo modulem
:grasscmd:`v.db.addcolumn` v kombinaci s :grasscmd:`v.db.update`.

.. code-block:: bash

   v.db.addcolumn map=hpj_kpp_land columns="KC double"
   v.db.update map=hpj_kpp_land column=KC value="K * C"

Výsledek opět zkontrolujeme.

.. code-block:: bash

   db.select sql="select cat,K,C,KC from hpj_kpp_land where cat <= 3"

.. code-block:: bash

   cat|K|C|KC
   1|0.13|0.19|0.0247
   2|0.13|0.19|0.0247
   3|0.13|0.19|0.0247
   ...

V dalším kroku vektorovou mapu převedeme na rastrovou reprezentaci
modulem :grasscmd:`v.to.rast`. Pro zachovaní informací použijeme
prostorové rozlišení *1 m* (:grasscmd:`g.region`,
viz. :skoleni:`výpočetní region
<grass-gis-zacatecnik/intro/region.html>` ze školení GRASS GIS pro
začátečníky).

.. code-block:: bash
   
   g.region raster=dmt res=1 
   v.to.rast input=hpj_kpp_land output=hpj_kpp_land_kc use=attr attribute_column=KC

Pomocí modulu :grasscmd:`r.resamp.stats` provedeme převzorkovaní na
prostorové rozlišení DMT *10m* a to na základě průměru hodnot
vypočítaného z hodnot okolních buněk. Tímto postupom zabráníme ztrátě
informací, ke kterému by došlo při přímém převodu na rastr s
rozlišením *10m*. Při rasterizaci se totiž hodnota buňky rastru
odvozuje na základě polygonu, který prochází středem buňky anebo na
základě polygonu, který zabírá největší část plochy buňky.

.. code-block:: bash
   
   g.region raster=dmt
   r.resamp.stats input=hpj_kpp_land_kc output=hpj_kpp_land_kc10 

Na obrázku :numref:`porovkn` je znázorněná část zájmového území, kde
možno vidět rastrovou vrstvu :map:`hpj_kpp_land_kc` před (vlevo dole)
a po použití modulu :grasscmd:`r.resamp.stats`.

.. _porovkn:

.. figure:: images/10a.png
   
   Část zájmového území s faktorem *KC* před a po převzorkovaní.
                      
Kvůli vizualizaci nastavíme vhodnou :skoleni:`tabulku barev
<grass-gis-zacatecnik/rastrova_data/tabulka-barev.html>` a kvůli
přehlednosti mapu přejmenujeme na :map:`kc` modulem
:grasscmd:`g.rename`. Výsledek je na :numref:`kc`.

.. code-block:: bash
                
   r.colors map=hpj_kpp_land_kc10 color=wave
   g.rename raster=hpj_kpp_land_kc10,kc

.. _kc:

.. figure:: images/11.png
   :class: small

   Faktor *KC* zahrnující vliv eroze půdy a vliv ochranného vlivu
   vegetačního pokrytu.

R a P faktor
^^^^^^^^^^^^

Hodnoty těchto parametrů nebudeme odvozovat jako ty předcházející. V
tomto případě jednoduše použijeme průmernou hodnotu ``R`` a ``P``
faktoru pro Českou republiku, t.j ``R = 40`` a ``P = 1``.

Výpočet průmerné dlouhodobé ztráty půdy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ztrátu půdy `G` vypočítame modulem :grasscmd:`r.mapcalc`
(:numref:`rmapcalc`), přičemž vycházíme ze vztahu, který byl uvedený v
:ref:`teoretické časti školení <vzorec-G>`.

.. _rmapcalc:

.. figure:: images/15.png
   :class: small

.. code-block:: bash
                
   r.mapcalc expr="g = 40 ∗ ls ∗ kc ∗ 1"
   r.colors -n -e map=g color=corine

Pro výslednou vrstvu zvolíme vhodnou barevnou škálu, přidáme legendu,
měřítko a mapu zobrazíme (:numref:`map-g`)

.. _map-g:

.. figure:: images/12.png
   :class: small

   Vrstva s hodnotami představujícími průměrnou dlouhodobou ztrátu
   půdy G v jednotkách :math:`t.ha^{-1} . rok^{-1}`.

.. note:: Na :numref:`map-g` je maximální hodnota v legendě *1*. Je to
    pouze z důvodu, aby byl výsledek přehledný a korespondoval s
    barvami v mapě. V skutečnosti parametr ``G`` nabývá hodnot až
    *230*, při takovémto rozsahu by byla stupnice v legendě
    jednobarevná (v našem případě červená).  Změnit rozsah intervalu v
    legendě bylo možné nastavením parametru *range*, konkrétněji
    příkazem :code:`d.legend raster=g range=0,1`.

Průměrná hodnota ztráty pro povodí
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Na určení průměrné hodnoty a sumy ztráty pro každé částečné povodí
využijeme modul :grasscmd:`v.rast.stats`. Klíčovou vrstvou je
vektorová mapa povodí :map:`povodi_iv`, kde nastavíme pro nově
vytvořený sloupec prefix :item:`g_`. Z těchto hodnot potom modulem
:grasscmd:`v.db.univar` vypočítáme statistiky průměrných hodnot ztráty
půdy.

.. code-block:: bash
                
   v.rast.stats map=povodi_iv raster=g column_prefix=g method=average
   v.db.univar map=povodi_iv column=g_average

.. note:: Vektorová vrstva povodí musí být umístěna v aktuálním
          mapsetu. Pokud například pracujeme v jiném mapsetu, stačí
          když ji přidáme z mapsetu :mapset:`PERMANENT` a následně v
          menu pravým kliknutím na mapě zvolíme :item:`Make a copy in
          the current mapset`.

Pro účely vizualizace vektorovou vrstvu převedeme na rastr, pomocí
modulu :grasscmd:`r.colors` nastavíme vhodnou tabulku barev a výsledek
prezentujeme, viz. :numref:`g-average`.

.. code-block:: bash
   
   v.to.rast input=povodi_iv output=pov_avg_G use=attr attribute_column=g_average
   r.colors -e map=pov_avg_G color=bgyr

.. _g-average:

.. figure:: images/13.png

   Povodí s průměrnými hodnotami ztráty půdy

.. note:: Z důvodu přehlednosti je opět interval v legendě
          upravený. Maximální hodnota průmerné ztráty půdy na povodí
          je až *0.74* (v jednotkách :math:`t.ha^{-1} . rok^{-1}`)
    
Zahrnutí prvků prerušujících odtok
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pro výpočet uvedený výše vychází ztráta půdy v některých místech
enormně vysoká. To je způsobené tím, že ve výpočtech nejsou zahrnuté
liniové a plošné prvky přerušující povrchový odtok. Těmito prvky jsou
především budovy, příkopy dálnic a silnic, železniční tratě anebo
ploty lemující pozemky.

Abysme zjistili přesnější hodnoty, je nutné tyto prvky do výpočtu
zahrnout. Pro tento účel použijeme masku liniových a plošných prvků
přerušujících odtok :map:`maska.pack` a vypočítame nové hodnoty LS
faktoru a ztráty půdy. Vstupem bude :map:`dmt` bez prvků přerušujících
odtok (:numref:`dmt-m`).

.. todo:: Tuto část je potřeba rozšířit. Maska by se dala určit z
          RÚIAN, a pod.
          
.. code-block:: bash
   
   r.unpack -o input=MASK.pack output=maska
   r.mask raster=maska
   r.terraflow elevation=dmt filled=dmt_fill_m direction=dir_m swatershed=sink_maccumulation=accu_m tci=tci_m

.. _dmt-m:

.. figure:: images/14a.png
   :class: small

   Vrstva digitálního modelu terénu vstupujícího do výpočtu bez prvků
   přerušujících odtok.


Dále dopočítame faktor *LS* a následně *G*.

.. code-block:: bash

   r.mapcalc expr="ls_m = pow(accu_m * (10.0 / 22.13), 0.6) * pow(sin(svah * (3.1415926/180)) / 0.09, 1.3)"
   r.mapcalc expr="g_m = 40 ∗ ls_m ∗ kc ∗ 1"
   
   r.colors map=ls_m color=wave
   r.colors -n -e map=g_m color=corine

V posledním kroku vymažeme masku, výsledky zobrazíme a porovnáme
(:numref:`ls-porov` a :numref:`g-porov`).
             
.. _ls-porov:

.. figure:: images/ls_porov.png
   :scale: 55%
     
   Porovnání hodnot faktoru LS bez ohledu na prvky přerušující odtok
   (vlevo) a s prvky přerušujícími odtok (vpravo).

.. _g-porov:

.. figure:: images/g_porov.png
   :scale: 57%

   Porovnaní výsledků USLE bez ohledu na prvky přerušující odtok
   (vlevo) a s prvky přerušujícími odtok (vpravo).

Průměrná hodnota ztráty pro povodí s prvky přerušujícími odtok
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Opět využijeme modul :grasscmd:`v.rast.stats`. Vektorové mapě povodí
:map:`povodi_iv` nastavíme prefix :item:`g_m` pro nově vytvořený
sloupec a potom modulem :grasscmd:`v.db.univar` zobrazíme statistiky
průměrných hodnot ztráty půdy. Výsledek v rastrové podobě je na
:numref:`g-m-average`.

.. code-block:: bash
                
   v.rast.stats map=povodi_iv raster=g_m column_prefix=g_m method=average
   v.db.univar map=povodi_iv column=g_m_average
   
   v.to.rast input=povodi_iv output=pov_avg_G_m use=attr attribute_column=g_m_average
   r.colors -e map=pov_avg_G_m color=bgyr

.. _g-m-average:

.. figure:: images/16.png

   Povodí s průměrnými hodnotami ztráty půdy s uvážením prvků,
   které přerušují odtok.

Na závěr vypočítáme rozdíly (modul :grasscmd:`r.mapcalc`) výsledných
vrstev bez a s uvážením prvků, které přerušují odtok pro faktor *LS*,
hodnoty představující průměrnou dlouhodobou ztrátu půdy *G* a povodí s
průměrnými hodnotami ztráty půdy *G_pov*. Nazveme je :map:`delta_ls`,
:map:`delta_g` a :map:`delta_pov_avg` a nastavíme barevnou stupnici
:item:`differences`. Viz. :numref:`diff`.

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

   Znázornění rozdílů rastrových vrstev LS, G a G_pov, které
   vznikly bez uvážení a s uvážením prvků, které přerušují odtok.
 
Poznámky
--------

GRASS nabízí na výpočet USLE dva užitečné moduly :grasscmd:`r.uslek` a
:grasscmd:`r.usler`.
