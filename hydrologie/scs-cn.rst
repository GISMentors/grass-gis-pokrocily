1. Metóda SCS CN
================

Teoretické východiská
---------------------

Ide o výpočet odtokovej straty z povodia. Metóda bola vypracovaná
službou na ochranu pôd *Soil Conservation Service* (:wikipedia:`SCS CN
<Metoda CN křivek>`) v USA. Objem zrážok je na objem odtoku prevedený
<<<<<<< HEAD
podľa čísel odtokových kriviek *CN*, ktoré sú tabelizované na
základe hydrologických vlastností pôd *HydrSk*. Metóda zohľadňuje
závislosť retencie (zadržiavanie vody) od hydrologických vlastností pôd,
počiatočné nasýtenie a spôsob využívania pôdy. Číslo *CN* krivky
reprezentuje teda vlastnosť povodia. Obvykle nadobúda hodnoty :item:`30`,
t.j. veľké straty až :item:`100`, t.j. malé straty.

Číslo *CN* závisí od kombinácie hydrologickej skupiny pôdy a spôsobu využitia
územia v danom mieste. Kód hydrologickej skupiny pôdy je získaný z dát hlavných
pôdnych jednotiek (presnejší spôsob) alebo dát komplexného prieskumu pôd (tam, 
kde informácie o hlavných pôdnych jednotkách k dispozícii nie sú).
=======
podľa čísel odtokových kriviek *CN*, ktoré sú tabelizované na základe
hydrologických vlastností pôd *HydrSk*. Metóda zohľadňuje závislosť
retencie (zadržiavanie vody) od hydrologických vlastností pôd,
počiatočné nasýtenie a spôsob využívania pôdy. Číslo *CN* krivky
reprezentuje teda vlastnosť povodia. Obvykle nadobúda hodnoty
:item:`30`, t.j. veľké straty až :item:`100`, t.j. malé straty.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

Základné symboly:
-----------------

 * :math:`CN` ... číslo odtokovej krivky
 * :math:`A` ... maximálna potenciálna strata z povodia, resp. výška vody 
   zadržaná v povodí; ostatné je odtok (:math:`mm`)
 * :math:`I_a` ... počiatočná strata z povodia, keď ešte nedochádza k odtoku
   (:math:`mm`)
 * :math:`H_s` ... návrhová výška zrážky, záťažový stav (:math:`mm`)
 * :math:`H_o` ... výška priameho odtoku (:math:`mm`)
 * :math:`P_p` ... výmera elementárnej plochy (:math:`m^2`)
 * :math:`O_p` ... objem priameho odtoku (:math:`m^3`)

Platí, že pomer medzi skutočnou a maximálnou stratou z povodia je rovnaký
ako pomer odtoku a zrážky, ktorá je redukovaná o počiatočné straty [:ref:`3<o3>`].

.. math::

   \frac{O_p}{A}=\frac{H_o}{H_s-I_a}

Vstupné dáta
------------

 * :map:`hpj` - vektorová vrstva hlavných pôdnych jednotiek,
 * :map:`kpp` - vektorová vrstva komplexného prieskumu pôd,
<<<<<<< HEAD
 * :dbtable:`hpj_hydrsk.dbf`, :dbtable:`sum_kpp2hydrsk.dbf` - pomocné číselníky 
   s hydrologickými skupinami pôd,
 * :map:`Land_Use` - vektorová vrstva využitia územia,
 * :map:`A07_Povodi_IV` - vektorová vrstva povodí IV. rádu s návrhovými
   zrážkami :math:`H_s` (doba opakovania 5, 10, 20, 50 a 100 rokov).
=======
 * :dbtable:`hpj_hydrsk.dbf`, :dbtable:`sum_kpp2hydrsk.dbf` - pomocné číselníky s hydrologickými skupinami pôd,
 * :map:`land_use` - vektorová vrstva využitia územia,
 * :map:`A07_Povodi_IV` - vektorová vrstva povodí IV. rádu s návrhovými zrážkami :math:`H_s` (doba opakovania 5, 10, 20, 50 a 100 rokov).
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

Navrhovaný postup:
------------------

<<<<<<< HEAD
1. príprava potrebných dát pre výpočet v prostredí GIS (rastrová vrstva s kódmi 
   :math:`CN`, raster s hodnotami :math:`H_s` a raster s výmerou :math:`P_p` 
   pre elementárne plochy v :math:`m^2`),
2. výpočet parametra :math:`A`, ktorý je funkciou :math:`CN`,
3. výpočet parametra :math:`I_a`, ktorý je funkciou :math:`A`,
4. výpočet parametra :math:`H_o`, ktorý je funkciou :math:`H_s` a :math:`A`,
5. výpočet parametra :math:`O_p`, ktorý je funkciou :math:`P_p` a :math:`H_o`.
=======
 1. príprava potrebných dát pre výpočet v prostredí GIS (rastrová
    vrstva s kódmi CN, raster s hodnotami :math:`H_s` a raster s
    výmerou :math:`P_p` pre elementárne plochy v :math:`m^2`),
 2. výpočet parametra :math:`A`, ktorý je funkciou CN,
 3. výpočet parametra :math:`I_a`, ktorý je funkciou :math:`A`,
 4. výpočet parametra :math:`H_o`, ktorý je funkciou :math:`H_s` a :math:`A`,
 5. výpočet parametra :math:`O_p`, ktorý je funkciou :math:`P_p` a :math:`H_o`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. _schema:

.. figure:: images/schema_a.PNG
   :class: middle

   Grafická schéma postupu

<<<<<<< HEAD
.. note:: Ako vyplýva z :num:`#schema`, príprave rastrovej vrstvy s kódmi CN 
	  predchádza odvodenie hydrologických skupín pôd *HydrSk* a jej 
	  priestorové prekrytie s vrstvou využitia krajinnej pokrývky *land*, 
	  čím sa získa jedinečná kombinácia *hpj_kpp_land*, resp. *HydrSk_land*.
=======
.. todo:: Nechybí v horní pravé části šipky? Možná by se do diagramu
          hodilo graficky znázornit jednotlivé kroky (třeba
          obdélníkem)? Dále sjednotit názvy vstupních souborů -
          diagram a návod.
                  
.. note:: Ako vyplýva z :num:`#schema`, príprave rastrovej vrstvy s
          kódmi CN predchádza odvodenie hydrologických skupín pôd
          *HydrSk* a jej priestorové prekrytie s vrstvou využitia
          krajinnej pokrývky *land_use (LU)*, čím sa získa jedinečná kombinácia
          *HydrSk_land*.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

Postup spracovania v GRASS GIS
------------------------------

Krok 1
^^^^^^

<<<<<<< HEAD
V prvom kroku zjednotíme vrstvu hlavných pôdnych jednotiek a komplexného
prieskumu pôd. Použijeme modul :grasscmd:`v.overlay` a operáciu prekrývania
*union*.
=======
V prvom kroku zjednotíme vrstvu hlavných pôdnych jednotiek a
komplexného prieskumu pôd. Použijeme modul :grasscmd:`v.overlay` a
operáciu prekrývania *union*.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

   v.overlay ainput=hpj binput=kpp operator=or output=hpj_kpp

<<<<<<< HEAD
Importujeme čiselníky.

=======
Pomocí modulu :grasscmd:`db.in.ogr` importujeme čiselníky.
                
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
.. code-block:: bash

   db.in.ogr input=hpj_hydrsk.dbf output=hpj_hydrsk
   db.in.ogr input=sum_kpp2hydrsk.dbf output=kpp_hydrsk

<<<<<<< HEAD
Pre kontrolu prezrieme obsah importovaných číselníkov (tabuliek)
v prostredí GRASS GIS, prípadne aspoň ich stĺpcov. Použijeme moduly
=======
Pre kontrolu prezrieme obsah importovaných číselníkov (tabuliek) v
prostredí GRASS GIS, prípadne aspoň ich stĺpcov. Použijeme moduly
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
:grasscmd:`db.select` a :grasscmd:`db.columns`.

.. code-block:: bash

   db.select table=hpj_hydrsk
   db.select table=kpp_hydrsk

   db.columns table=hpj_hydrsk
   db.columns table=kpp_hydrsk
<<<<<<< HEAD

.. note::

   V atribútovej tabuľke hlavných pôdnych jednotiek :map:`hpj_hydrsk` je po
   importe dátový typ atribútu :dbcolumn:`HPJ` ako *type: DOUBLE PRECISION*
   (príkaz :code:`db.describe table=hpj_hydrsk`); je potrebné prekonvertovať
   ho na celočíselný typ, t.j. *type: INTEGER* (kvôli spájaniu tabuliek
   a číselníkov pomocou :grasscmd:`v.db.join`). Použijeme **ALTER**
   na vytvorenie atribútu :dbcolumn:`HPJ_key` a **UPDATE** na naplnenie
   hodnôt atribútu.
=======
   
.. note:: 
   
   V atribútovej tabuľke hlavných pôdnych jednotiek :map:`hpj_hydrsk`
   je po importe dátový typ atribútu :dbcolumn:`HPJ` ako *type: DOUBLE
   PRECISION* (príkaz :code:`db.describe table=hpj_hydrsk`); je
   potrebné prekonvertovať ho na celočíselný typ, t.j. *type: INTEGER*
   (kvôli spájaniu tabuliek a číselníkov pomocou
   :grasscmd:`v.db.join`). Použijeme :sqlcmd:`ALTER` na vytvorenie atribútu
   :dbcolumn:`HPJ_key` a :sqlcmd:`UPDATE` na naplnenie hodnôt atribútu. SQL
   příkazy provedeme pomocí modulu :grasscmd:`db.execute`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

   db.execute sql="alter table hpj_hydrsk add column HPJ_key int"
   db.execute sql="update hpj_hydrsk set HPJ_key = cast(HPJ as int)"
<<<<<<< HEAD

Po úprave tabuľky :dbtable:`hpj_hydrsk` môžeme túto tabuľku pripojiť
k atribútom vektorovej mapy :map:`hpj_kpp` pomocou kľúča, konkrétne
=======
   
Po úprave tabuľky :dbtable:`hpj_hydrsk` môžeme túto tabuľku pripojiť k
atribútom vektorovej mapy :map:`hpj_kpp` pomocou kľúča, konkrétne
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
atribútu :dbcolumn:`HPJ_key`.

.. code-block:: bash

   v.db.join map=hpj_kpp column=a_HPJ other_table=hpj_hydrsk
   other_column=HPJ_key

<<<<<<< HEAD
Atribúty v tabuľke :dbtable:`hpj_kpp` po spojení skontrolujeme či obsahujú
stĺpce z číselníka a následne doplníme chýbajúce informácie o
hydrologickej skupine :dbcolumn:`HydrSk` pomocou :map:`kpp_hydrsk`. Doplníme
ich zo stĺpca :dbcolumn:`First_Hydr` vrstvy komplexného prieskumu
pôd. Využijeme modul :grasscmd:`db.execute` a SQL príkaz **JOIN**.
=======
Atribúty v tabuľke :dbtable:`hpj_kpp` po spojení skontrolujeme či
obsahujú stĺpce z číselníka a následne doplníme chýbajúce informácie o
hydrologickej skupine :dbcolumn:`HydrSk` pomocou
:map:`kpp_hydrsk`. Doplníme ich zo stĺpca :dbcolumn:`First_Hydr`
vrstvy komplexného prieskumu pôd. Využijeme modul
:grasscmd:`db.execute` a SQL príkaz :sqlcmd:`JOIN`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

    db.execute sql="UPDATE hpj_kpp_1 SET HydrSk = (
    SELECT b.First_hydr FROM hpj_kpp_1 AS a JOIN kpp_hydrsk as b
    ON a.b_KPP = b.KPP) WHERE HydrSk IS NULL"

Výsledok môže vyzerať nasledovne.

.. figure:: images/scs-cn-db-join.png

   Atribútový dotaz s výsledkom hydrologickej skupiny pôd

Prezrieme všetky informácie v atribútovej tabuľke :map:`hpj_kpp` cez
<<<<<<< HEAD
*SQL Query BUILDER* a overíme či všetky hodnoty o hydrologickej skupine
sú vyplnené.
=======
*SQL Query Builder* a overíme či všetky hodnoty o hydrologickej
skupine sú vyplnené.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

    SELECT cat,HydrSk FROM hpj_kpp_1 WHERE hydrSk = "NULL"

<<<<<<< HEAD
Nastavíme :skoleni:`tabuľku farieb <grass-gis-zacatecnik/raster/tabulka-barev.html>` 
pre jednotlivé skupiny pomocou modulu :grasscmd:`v.colors`. Kódy nemôžu byť 
použité, lebo tento modul podporuje iba celočíselné hodnoty, preto je potrebné
vytvoriť nový atribút s jedinečnými hodnotami pre kódy. Nazveme ho
:dbcolumn:`HydrSk_key`) a bude obsahovať čísla 1 až 7 prislúchajúce
kódom A až D. Použijeme moduly :grasscmd:`v.db.addcolumn` a
:grasscmd:`db.execute` a príkaz **UPDATE** jazyka SQL.
=======
Nastavíme :skoleni:`tabuľku farieb
<grass-gis-zacatecnik/rastrova_data/tabulka-barev.html>` pre jednotlivé
skupiny pomocou modulu :grasscmd:`v.colors`. Kódy nemôžu byť použité,
lebo tento modul podporuje iba celočíselné hodnoty, preto je potrebné
vytvoriť nový atribút s jedinečnými hodnotami pre kódy (nazveme ho
:dbcolumn:`HydrSk_key`). Bude obsahovať čísla 1 až 7 prislúchajúce
kódom A až D. Použijeme moduly :grasscmd:`v.db.addcolumn` a
:grasscmd:`db.execute` a príkaz :sqlcmd:`UPDATE` jazyka SQL.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

    v.db.addcolumn map=hpj_kpp columns=HydrSk_key int

    db.execute sql="update hpj_kpp_1 set HydrSk_key = 1 where HydrSk = 'A';
    update hpj_kpp_1 set HydrSk_key = 2 where HydrSk = 'AB';
    update hpj_kpp_1 set HydrSk_key = 3 where HydrSk = 'B';
    update hpj_kpp_1 set HydrSk_key = 4 where HydrSk = 'BC';
    update hpj_kpp_1 set HydrSk_key = 5 where HydrSk = 'C';
    update hpj_kpp_1 set HydrSk_key = 6 where HydrSk = 'CD';
    update hpj_kpp_1 set HydrSk_key = 7 where HydrSk = 'D'"

<<<<<<< HEAD
.. note:: Nový stĺpec možno pridať aj pomocou :skoleni:`správcu 
	  atribútových dát <grass-gis-zacatecnik/vector/atributy.html>`.
=======
.. note:: Nový stĺpec možno pridať aj pomocou :skoleni:`správcu
          atribútových dát
          <grass-gis-zacatecnik/vektorova_data/atributy.html>`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

Do textového súboru :file:`colors.txt` vložíme pravidlá pre vlastnú
farebnú stupnicu pre jednotlivé kategórie.

.. code-block:: bash

   1 red
   2 green
   3 yellow
   4 blue
   5 brown
   6 orange
   7 purple

Modulom :grasscmd:`g.region` nastavíme výpočtový región
(napr. :map:`hpj_kpp`), konvertujeme vektorovú vrstvu na rastrovú,
<<<<<<< HEAD
priradíme farebnú škálu a doplníme mimorámové údaje ako legendu a mierku.

.. note:: Vektorovú vrstvu konvertujeme kvôli tomu, lebo zobraziť legendu je 
	  možné len pre rastrové dáta.
=======
priradíme farebnú škálu a doplníme mimorámové údaje: legendu a mierku
(viz školení GRASS GIS pro začátečníky kapitola :skoleni:`Mapové
elementy <grass-gis-zacatecnik/ruzne/mapove-elementy.html>`).

.. note:: Vektorovú vrstvu konvertujeme kvôli tomu, lebo zobraziť
          legendu je možné len pre rastrové dáta.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

   g.region vector=hpj_kpp
   v.to.rast input=hpj_kpp output=hpj_kpp_rst use=attr
   attribute_column=HydrSk_key

.. figure:: images/1a.png
   :class: middle

   Výsledná vizualizácia hydrologických skupín pôd (1: A, 2: AB, 3:
   B, 4: BC, 5: C, 6: CD a 7: D)

<<<<<<< HEAD
Pridáme informácie o využití územia pre každú plochu pomocou operácie prieniku 
*intersection* s dátovou vrstvou o krajinnej pokrývke :map:`Land_Use`.
=======
Pridáme informácie o využití územia pre každú plochu pomocou operácie
priniku *intersection* s dátovou vrstvou o krajinnej pokrývke
:map:`land_use`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block:: bash

   v.overlay ainput=hpj_kpp binput=land_use operator=and output=hpj_kpp_land

<<<<<<< HEAD
Pridáme stĺpec :dbcolumn:`LU_HydrSk` s informáciami o využití územia
a hydrologickej skupine pre každú elementárnu plochu. Hodnoty budú v
=======
Pridáme stĺpec :dbcolumn:`LU_HydrSk` s informáciami o využití územia a
hydrologickej skupine pre každú elementárnu plochu. Hodnoty budú v
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
tvare *VyužitieÚzemia_KodHydrologickejSkupiny*, t.j. *LU_HydrSk*.

.. code-block::bash

   v.db.addcolumn map=hpj_kpp_land columns="LU_HydrSk text"
   db.execute sql="update hpj_kpp_land_1 set LU_HydrSk = b_LandUse || '_'
   || a_HydrSk"

<<<<<<< HEAD
.. note: Túto operáciu je možné vykonať aj pomocou :skoleni:`správcu 
	 atribútových dát <grass-gis-zacatecnik/vector/atributy.html>` (`Field
	 Calculator`)

Pomocou modulu :grasscmd:`db.select` alebo pomocou :skoleni:`správcu 
atribútových dát <grass-gis-zacatecnik/vector/atributy.html>` vypíšeme
=======
.. note: Túto operáciu je možné vykonať aj pomocou :skoleni:`správcu
   atribútových dát <grass-gis-zacatecnik/vektorova_data/atributy.html>`
   (`Field Calculator`)

Pomocou modulu :grasscmd:`db.select` alebo pomocou :skoleni:`správcu
atribútových dát <grass-gis-zacatecnik/vektorova_data/atributy.html>` vypíšeme
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
počet všetkých kombinácií v stĺpci :dbcolumn:`LU_HydrSk`.

.. code-block::bash

   db.select sql="select count(*) as comb_count from (select LU_HydrSk from
   hpj_kpp_land_1 group by LU_HydrSk)"`

.. figure:: images/2a.png
   :class: middle

<<<<<<< HEAD
   Zobrazenie časti atribútovej tabuľky a výpis počtu kombinácií
   krajinnej pokrývky a hydrologickej skupiny

Určíme odpovedajúce hodnoty :math:`CN`. Importujeme ich zo súboru
:dbtable:`LU_CN.xls` a následne pripojíme pomocou :grasscmd:`v.db.join`.

=======
   Zobrazenie časti atribútovej tabuľky a výpis počtu kombinácií krajinnej pokrývky a hydrologickej skupiny
 
Určíme odpovedajúce hodnoty CN. Importujeme ich zo súboru
:dbtable:`LU_CN.xls` a následne pripojíme pomocou
:grasscmd:`v.db.join`.
 
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
.. code-block::bash

   db.in.ogr input=LU_CN.xls output=lu_cn
   v.db.join map=hpj_kpp_land column=LU_HydrSk other_table=lu_cn
   other_column=LU_HydrSk

<<<<<<< HEAD
Výsledné informácie ako kód hydrologickej skupiny, kód krajinnej pokrývky
a kód :math:`CN` zobrazíme v atribútovej tabuľke SQL dotazom 
=======
Výsledné informácie ako kód hydrologickej skupiny, kód krajinnej
pokrývky a kód CN zobrazíme v atribútovej tabuľke SQL dotazom
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
:code:`SELECT cat,a_HydrSk,b_LandUse,CN FROM hpj_kpp_land_1`.

Následne vytvoríme rastrovú vrstvu s kódmi :math:`CN`.

.. cole-block::bash

   g.region vector=hpj_kpp_land
   v.to.rast input=hpj_kpp_land output=hpj_kpp_land_rst use=attr
   attribute_column=CN
   r.colors -e map=hpj_kpp_land_rst color=aspectcolr

.. figure:: images/3a.png
   :class: middle

<<<<<<< HEAD
   Kódy :math:`CN` pre každú elementárnu plochu krajinnej pokrývky v záujmovom
=======
   Kódy CN pre každú elementárnu plochu krajinnej pokrývky v záujmovom
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
   území

Atribútová tabuľka vrstvy povodí obsahuje údaje o návrhových zrážkach
s dobou opakovania 5, 10, 20, 50 a 100 rokov. Je potrebné pridať tieto
informácie ku každej elementárnej ploche.

.. figure:: images/5a.png
   :class: middle

   Atribúty súvisiace s návrhovými zrážkami s rôznou dobou opakovania

<<<<<<< HEAD
Vrstvu :map:`hpj_kpp_land` zjednotíme s vrstvou povodí :map:`A07_Povodi_IV`,
na čo využijeme modul :grasscmd:`v.overlay`.
=======
Vrstvu :map:`hpj_kpp_land` zjednotíme s vrstvou povodí
:map:`A07_Povodi_IV`, na čo využijeme modul :grasscmd:`v.overlay`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block::bash

   v.overlay ainput=hpj_kpp_land binput=A07_Povodi_IV operator=or
   output=hpj_kpp_land_pov`

Po zjednotení vidíme, že došlo k rozdeleniu územia na menšie plochy (87
237, 91 449). Presný počet možno zistiť použitím :grasscmd:`db.select`.

<<<<<<< HEAD
.. code-block::bash
=======
Po zjednotení vidíme, že došlo k rozdeleniu územia na menšie plochy
(87 237, 91 449). Presný počet možno zistiť použitím
:grasscmd:`db.select`.
 
.. code-block:: bash
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

   db.select sql="select count (*) as elem_pocet from hpj_kpp_land_1"
   db.select sql="select count (*) as elem_pocet from hpj_kpp_land_pov_1"

.. figure:: images/6a.png
   :class: small

   Počet elementárnych plôch pred a po zjednotení s vrstvou povodí

Kroky 2 a 3
^^^^^^^^^^^

<<<<<<< HEAD
Pre každú elementárnu plochu vypočítame jej výmeru, parameter :math:`A`
(maximálna strata) a parameter :math:`I_{a}` (počiatočná strata, čo je
5 % z :math:`A`)
=======
Pre každú elementárnu plochu vypočítame jej výmeru, parameter
:math:`A` (maximálna strata) a parameter :math:`I_{a}` (počiatočná
strata, čo je 5 % z :math:`A`)
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. math::

   A = 25.4 \times (\frac{1000}{CN} - 10)

.. math::

   I_a = 0.2 \times A

Do atribútovej tabuľky `hpj_kpp_land_pov` pridáme nové stĺpce
:dbcolumn:`vymera`, :dbcolumn:`A`, :dbcolumn:`I_a` výpočítame výmeru,
parameter :math:`A` a parameter :math:`I_{a}`.

.. code-block::bash

   v.db.addcolumn map=hpj_kpp_land_pov columns="vymera double,A double,I_a
   double"
   v.to.db map=hpj_kpp_land_pov option=area columns=vymera
   v.db.update map=hpj_kpp_land_pov column=A value="24.5 * (1000 / a_CN - 10)"
   v.db.update map=hpj_kpp_land_pov column=I_a value="0.2 * A"

Kroky 4 a 5
^^^^^^^^^^^

<<<<<<< HEAD
.. note:: V ďalších krokoch budeme uvažovať priemerný úhrn návrhovej zrážky 
	  :math:`H_{s}` = 32 mm. Pri úhrne s dobou opakovania 2 roky (atribút
	  :dbcolumn:`H_002_120`) či dobou 5, 10, 20, 50 alebo 100 rokov by bol 
	  postup obdobný.

Pridáme ďalšie nové stĺpce do atribútovej tabuľky pre parametre :math:`H_{o}`
a :math:`O_{p}` a vypočítame ich hodnoty pomocou :grasscmd:`v.db.update`.
=======
.. note:: V ďalších krokoch budeme uvažovať priemerný úhrn návrhovej
          zrážky :math:`H_{s}` = 32 mm. Pri úhrne s dobou opakovania 2
          roky (atribút :dbcolumn:`H_002_120`) či dobou 5, 10, 20, 50
          alebo 100 rokov by bol postup obdobný.

.. code-block::bash

   db.select sql="select count(*) as pocet from hpj_kpp_land_pov_1 where ((32 < I_a) or (b_H_002_120 < I_a))" 

Pridáme ďalšie nové stĺpce do atribútovej tabuľky pre parametre
:math:`H_{o}` a :math:`O_{p}` a vypočítame ich hodnoty pomocou
:grasscmd:`v.db.update`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. math::

   H_O = \frac{(H_S − 0.2 \times A)^2}{H_S + 0.8 \times A}

.. note:: Hodnota v čitateli musí byť kladná, resp. nesmieme umocňovať záporné 
	  číslo. V prípade, že čitateľ je záporný, výška priameho odtoku je
	  rovná nule. Na vyriešenie tejto situácie si pomôžeme novým stĺpcom
	  v atribútovej tabuľke, ktorý nazveme :dbcolumn:`HOklad`. 

.. math::

   O_P = P_P \times \frac{H_O}{1000}

.. code-block::bash

   v.db.addcolumn map=hpj_kpp_land_pov columns="HOklad double, HO double, 
   OP double"

   v.db.update map=hpj_kpp_land_pov column=HOklad value="((32 - 0.2 * A) *
   (32 - 0.2 * A)) / (32 + 0.8 * A)"
   


   v.db.update map=hpj_kpp_land_pov column=HO value="((32 - 0.2 * A) *
   (32 - 0.2 * A)) / (32 + 0.8 * A)"
   v.db.update map=hpj_kpp_land_pov column=OP value="vymera * (HO / 1000)"


Výsledky zobrazíme v rastrovej podobe.

.. code-block::bash

   v.to.rast input=hpj_kpp_land_pov output=HO use=attr attribute_column=HO
   v.to.rast input=hpj_kpp_land_pov output=OP use=attr attribute_column=OP

.. figure:: images/7a.png
   :class: middle

   Výška v mm vľavo a objem v :math:`m^{3}` vpravo priameho odtoku pre
   elementárne plochy

<<<<<<< HEAD
Vypočítame a zobrazíme priemerné hodnoty priameho odtoku pre jednotlivé povodia. 
Pritom je potrebné nastaviť rozlíšenie výpočtového regiónu, prekopírovať mapu 
povodí do aktuálneho mapsetu a nastaviť vhodnú :skoleni:`farebnosť výsledku 
<grass-gis-zacatecnik/raster/tabulka-barev.html>`.
=======
Vypočítame a zobrazíme priemerné hodnoty priameho odtoku pre
jednotlivé povodia. Pritom je potrebné nastaviť rozlíšenie výpočtového
regiónu, prekopírovať mapu povodí do aktuálneho mapsetu a nastaviť
vhodnú :skoleni:`farebnosť výsledku
<grass-gis-zacatecnik/rastrova_data/tabulka-barev.html>`.
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

.. code-block::bash

   g.region vector=kpp@PERMANENT res=10
   g.copy vector=A07_Povodi_IV,A07_Povodi_IV
   v.rast.stats map=A07_Povodi_IV raster=HO column_prefix=ho
   v.to.rast input=A07_Povodi_IV output=HO_pov use=attr
   attribute_column=ho_average
   r.colors map=HO_pov color=bcyr

   v.rast.stats map=A07_Povodi_IV raster=OP column_prefix=op
   v.to.rast input=A07_Povodi_IV output=OP_pov use=attr
   attribute_column=op_average
   r.colors map=OP_pov color=bcyr

.. figure:: images/8a.png
   :class: middle

   Výpočet štatistických údajov pre každé povodie

.. figure:: images/9a.png
   :class: middle

<<<<<<< HEAD
   Priemerná výška odtoku v :math:`mm` a priemerný objem odtoku v :math:`m^{3}`
   povodí v záujmovom území
=======
   Priemerná výška odtoku v mm a priemerný objem odtoku v
   :math:`m^{3}` povodí v záujmovom území
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

Výstupné dáta:
--------------

<<<<<<< HEAD
* :map:`hpj_kpp` - zjednotenie :map:`hpj` a :map:`kpp` (atribúty aj z číselníka 
  :map:`hpj`),
* :map:`hpj_kpp_land` - prienik :map:`hpj_kpp` a :map:`LandUse`,
* :map:`hpj_kpp_rst` - raster s kódmi *HydrSk*,
* :map:`hpj_kpp_land_rast` - raster s kódmi *CN*,
* :map:`HO`, resp. :map:`HO_pov` - raster s výškou odtoku pre elementárne
  plochy, resp. pre povodia v mm,
=======
* :map:`hpj_kpp` - zjednotenie :map:`hpj` a :map:`kpp` (atribúty aj z
  číselníka :map:`hpj`),
* :map:`hpj_kpp_land` - prienik :map:`hpj_kpp` a :map:`LandUse`,
* :map:`hpj_kpp_rst` - raster s kódmi *HydrSk*,
* :map:`hpj_kpp_land_rast` - raster s kódmi *CN*,
* :map:`HO`, resp. :map:`HO_pov` - raster s výškou odtoku pre
  elementárne plochy, resp. pre povodia v mm,
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165
* :map:`OP`, resp. :map:`OP_pov` - raster s hodnotami objemu odtoku v
  :math:`m^{3}` pre elementárne plochy, resp. povodia.

Použité zdroje:
---------------

<<<<<<< HEAD
.. _o1:

[1] `Školení GRASS GIS pro pokročilé
<http://training.gismentors.eu/grass-gis-pokrocily/hydrologie/scs-cn.html>`_

.. _o2:

[2] `Index of /~landa/gis-zp-skoleni
<http://geo102.fsv.cvut.cz/~landa/gis-zp-skoleni>`_

.. _o3:

[3] Wikipédia : `Metóda CN kriviek
<https://cs.wikipedia.org/wiki/Metoda_CN_k%C5%99ivek>`_

.. _o5:
=======
[1] `Školení GRASS GIS pro pokročilé
<http://training.gismentors.eu/grass-gis-pokrocily/hydrologie/scs-cn.html>`_

[2] `Index of /~landa/gis-zp-skoleni
<http://geo102.fsv.cvut.cz/~landa/gis-zp-skoleni>`_

[3] Wikipédia : `Metóda CN kriviek
<https://cs.wikipedia.org/wiki/Metoda_CN_k%C5%99ivek>`_
>>>>>>> 39a966f1df3428544914d23386e852b6976b0165

[4] `HYDRO.upol.cz <http://hydro.upol.cz/?page_id=15>`_

