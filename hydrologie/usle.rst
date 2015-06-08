Průměrná dlouhodobá ztráta půdy
===============================

Vstupní data
------------

* vrstva povodí IV. řádu
* DMT v rozlišení 10 x 10 m
* HPJ - hlavní půdní jednotky z kódu BPEJ
* KPP - komplexní průzkum půd
* základní báze geografických dat - ZABAGED
* ortofotomapa
   
Postup
------

Nejprve vytvoříme z DMT (digitální model terénu) rastrovou mapu
znázorňující sklonové poměry ve stupních (*slope*), kterou později
použijeme pro výpočet :ref:`topografického faktoru LS <ls-faktor>`. Pro výpočet sklonových
poměrů použijeme :grasscmd:`r.slope.aspect`, viz
:skoleni:`topografické analýzy
<grass-gis-zacatecnik/raster/analyzy-povrchu.html>`. Nejprve je třeba
nastavit :skoleni:`výpočetní region
<grass-gis-zacatecnik/intro/region.html>` na základě vstupního DMT.

.. code-block:: bash
                
   g.region raster=dmt
   r.slope.aspect elevation=dmt slope=svah                           

.. figure:: images/dmt_svah.png

   DMT a míra svahu

Pomocí nástroje :grasscmd:`r.terraflow` vytvoříme rastrovou mapu směru
odtoku do sousední buňky s největším sklonem (:option:`direction`),
dále vyhlazený DMT (:option:`filled`) a rastrovou mapu znázorňující
akumulaci toku v každé buňce (:option:`accumulation`).

.. note:: Pro vytvoření vyhlazeného DMT lze doporučit Addons modul
          :grasscmdaddons:`r.hydrodem`. Pro výpočet směru odtoku lze
          použít alternativně modul :grasscmd:`r.fill.dir`, pro
          akumulaci odtoku :grasscmd:`r.watershed`.
          
Před výpočtem si nastavíme masku podle zájmového území, modul
:grasscmd:`r.mask`.

.. code-block:: bash

   r.mask raster=dmt
   r.terraflow elevation=dmt filled=dmt_fill direction=dir swatershed=sink accumulation=accu tci=tci

.. figure:: images/flow-dir.png

   Směr odtoku vytvořený modulem :grasscmd:`r.terraflow`

.. figure:: images/flow-accu.png

   Akumuluce odtoku vytvořená modulem :grasscmd:`r.terraflow`

.. _ls-faktor:
   
LS faktor
^^^^^^^^^

LS faktor lze vypočíst podle vzorce:

.. math::
   
   LS = (accu \times \frac{10.0}{22.13})^{0.6} \times (\frac{sin(slope \times \frac{pi}{180})}{0.09})^{1.3}
   
Pro tyto účely využijeme nástroj :grasscmd:`r.mapcalc` jako hlavní
nástroj :skoleni:`mapové algebry
<grass-gis-zacatecnik/raster/rastrova-algebra.html>` v systému GRASS.

V zápisu pro tento nástroj bude rovnice vypadat následovně:

.. code-block:: bash

   r.mapcalc expr="ls = pow(accu * (10.0 / 22.13), 0.6) * pow(sin(svah * (3.1415926/180)) / 0.09, 1.3)"

Nastavíme vhodně tabulku barev:

.. code-block:: bash

   r.colors -e map=ls color=colors.txt

::
      
   0 128:64:64
   1 255:128:64
   10 0:255:0
   20 0:128:128
   50 0:128:255
   
K faktor, C faktor
^^^^^^^^^^^^^^^^^^   

Hodnota K faktoru byla určena primárně dle HPJ z kódu BPEJ. Na
plochách bez kódu BPEJ byly hodnoty K faktoru určeny na základě
půdních typů a subtypů dle KPP.

Hodnota C faktoru zemědělsky využívaných oblastí byla zvolena na
základě průměrných hodnot pro jednotlivé plodiny.

Převodní tabulky nejprve naimportujeme modulem :grasscmd:`db.in.ogr`:

.. code-block:: bash
                
   db.in.ogr in=KPP_K.xls out=kpp_k
   db.in.ogr in=HPJ_K.xls out=hpj_k
   db.in.ogr in=LU_C.xls out=lu_c

Do atributové tabulky vektorové mapy :map:`hpj_kpp_land` (viz :ref:`návod
<hydrsk>` na její vytvoření) přídáme dva nové sloupečky :dbcolumn:`K`
a :dbcolumn:`C`. To provedeme pomocí :skoleni:`správce atributových
dat <grass-gis-zacatecnik/vector/atributy.html>` anebo modulu
:grasscmd:`v.db.addcolumn`.

.. code-block:: bash
                
   v.db.addcolumn map=hpj_kpp_land columns="K double"
   v.db.addcolumn map=hpj_kpp_land columns="C double" 

K atributové tabulce vektorové mapy :map:`hpj_kpp_land` připojíme pomocí
modulu :grasscmd:`v.db.join` informace z tabulky :dbtable:`hpj_k`.

.. code-block:: bash
                
   v.db.join map=hpj_kpp_land column=a_HPJ_key other_table=hpj_k other_column=HPJ  

Chybějící informace dle KPP doplníme SQL dotazem, který provedeme
modulem :grasscmd:`db.execute`.

.. code-block:: sql
   
   UPDATE hpj_kpp_land_1 SET K = (
   SELECT b.K FROM hpj_kpp_land_1 AS a JOIN kpp_k aS b ON a.a_b_KPP = b.KPP)
   WHERE K IS NULL

V dalším kroku doplníme hodnoty C faktoru z tabulky
:dbtable:`lu_c`.

.. code-block:: bash
                
   v.db.join map=hpj_kpp_land column=b_LandUse other_table=lu_c other_column=LU      

Dále do atributové tabulky přidáme nový atribut :dbcolumn:`KC`, do
kterého uložíme ``K * C``. To můžeme provést pomocí :skoleni:`správce
atributových dat <grass-gis-zacatecnik/vector/atributy.html>` anebo
modulem :grasscmd:`v.db.addcolumn` v kombinaci s
:grasscmd:`v.db.update`.

.. code-block:: bash

   v.db.addcolumn map=hpj_kpp_land columns="KC double"
   v.db.update map=hpj_kpp_land column=KC value="K * C"

Výsledek můžeme zkontrolovat jednoduchým SQL dotazem provedeným
modulem :grasscmd:`db.select`.

.. code-block:: bash

   db.select sql="select cat,K,C,KC from hpj_kpp_land_1 where cat < 10"

V dalším kroku vektorovou mapu převedeme do rastrové reprezentace
(:grasscmd:`v.to.rast`), pro zachování informace použijeme prostorové
rozlišení 1m (:grasscmd:`g.region`, viz :skoleni:`výpočetní region
<grass-gis-zacatecnik/intro/region.html>`).

.. code-block:: bash
   
   g.region raster=dmt res=1                                             
   v.to.rast input=hpj_kpp_land output=hpj_kpp_kc use=attr attribute_column=KC

Pomocí modulu :grasscmd:`r.resamp.stats` poté provedeme převzorkování
na prostorové rozlišení DMT 10 m a to na základě průměru hodnot
vypočteného z hodnot okolních buněk. Tímto postupem zamezíme ztrátě
informací, ke kterém by došlo při přímém převodu na rastr s rozlišením
10 m (při rasterizace se hodnota buňky rastru volí na základě
polygonu, který prochází středem buňky nebo na základě polygonu, který
zabírá největší část plochy buňky).

.. code-block:: bash

   g.region raster=dmt     
   r.resamp.stats input=hpj_kpp_kc output=hpj_kpp_kc10                        

Pro účely vizualizace nastavíme vhodnou :skoleni:`tabulku barev
<grass-gis-zacatecnik/raster/tabulka-barev.html>`:

.. code-block:: bash
                
   r.colors map=hpj_kpp_kc10 color=wave                                       

.. figure:: images/hpj_kpp_kc.png

   Výsledek rasterizace faktoru KC

R faktor, P faktor
^^^^^^^^^^^^^^^^^^   

Použijeme průměrnou hodnota R a P faktoru pro Českou republiku

.. math::

   R = 40 \, MJ.ha^{-1} .cm.h^{-1}
   
   P = 1

Výpočet průměrné dlouhodobé ztráty půdy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ztráta půdy `G` vypočteme jako:

.. math::
   
   G = R \times K \times L \times S \times C \times P

kde je:

* G průměrná dlouhodobá ztráta půdy (:math:`t.ha^{-1} . rok^{-1}`)
* R faktor erozní účinnosti deště (:math:`MJ.ha^{-1} .cm.h^{-1}`)
* K faktor erodovatelnosti půdy (:math:`t.h.MJ^{-1} .cm^{-1} .rok^{-1}`)
* L faktor délky svahu (-)
* S faktor sklonu svahu (-)
* C faktor ochranného vlivu vegetačního pokryvu (-)
* P faktor účinnosti protierozních opatření (-)

Přepis pro :grasscmd:`r.mapcalc`:

.. code-block:: bash
                
   r.mapcalc expr="g = 40 ∗ ls ∗ hpj_kpp_kc ∗ 1"

Průměrná hodnota ztráty pro povodí
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
   
Pro tuto operaci použijeme modul :grasscmd:`v.rast.stats`, pomocí
kterého vypočteme průměrné hodnoty a sumu ztráty půdy pro každé dílčí
povodí.

.. code-block:: bash
                
   v.rast.stats map=povodi_4 raster=g column_prefix=g_

Statistiku průměrných hodnot ztráty půdy můžete vytisknout pomocí
modulu :grasscmd:`v.db.univar`.

.. code-block:: bash

   v.db.univar map=povodi_4 column=g_average

Pro účely vizualizace nastavíme vhodnou tabulku barev pomocí modulu
:grasscmd:`v.colors`.

.. code-block:: bash
             
   v.colors map=povodi_4 use=attr column=g_average color=blues

.. figure:: images/povodi_g.png

   Povodí podle ztráty půdy
               
Zahrnutí prvků přerušujících odtok
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pro výpočet uvedený výše vychází ztráta půdy v některých místech
enormně vysoká. To je způsobeno tím, že ve výpočtu nejsou zahrnuty
liniové a plošné prvky přerušující povrchový odtok. Těmito prvky jsou
zejména budovy, příkopy silnic a cest, železniční tratě nebo zdi
lemující pozemky.

Pro zjištění přesnějších hodnot je tedy nutné tyto prvky do výpočtu
zahrnout. Proto byla na základě vybraných prvků vytvořena maska prvků
přerušujících odtok.

Masku liniových a plošných prvků spojíme pomocí modulu
:grasscmd:`v.patch`. Před spojením vektorových map rozšíříme liniové
prvky z důvodu nastavení masky pomocí modulu :grasscmd:`v.buffer`.

.. code-block:: bash

   v.buffer input=maska_linie output=maska_linie5 distance=5
   v.patch input=maska_linie5,maska_plochy output=maska
                          
Masku pro další analýzu nastavíme pomocí modulu :grasscmd:`r.mask`.

.. code-block:: bash

   r.mask -i vector=maska

S využitím masky vypočteme nově LS faktor a ztrátu půdy G.

.. code-block:: bash

   r.terraflow elevation=dmt filled=dmt_fill2 direction=dir2 swatershed=sink2 accumulation=accu2 tci=tci2
   r.mapcalc expr="ls2 = pow(accu2 * (10.0 / 22.13), 0.6) * pow(sin(svah * (3.1415926/180)) / 0.09, 1.3)"
   r.mapcalc expr="g2 = 40 ∗ ls2 ∗ hpj_kpp_kc ∗ 1"

.. todo:: doplnit porovnání, LS faktor vychází divně
             
::

   .. figure:: images/porovnani_ls.png
               
               Porovnání hodnot LS faktoru bez zohlednění prvků přerušujících
               odtok (vlelvo) a s prvky přerušujícími odtok (vpravo)

   .. figure:: images/porovnani_g.png

               Porovnání výsledků USLE bez zohlednění prvků přerušujících odtok
               (vlelvo) a s prvky přerušujícími odtok (vpravo)

Poznámky
--------

GRASS nabízí pro výpočet USLE dva užitečné moduly :grasscmd:`r.uslek`
a :grasscmd:`r.usler`.
