Vypublikování skriptu jako WPS procesu
======================================

Skript upravíme následovně:

#. Vytvoříme třídu :class:`Process` s rodičovskou třídou
   :class:`WPSProcess`, která je definována v rámci PyWPS (řádky
   :lcode:`17, 19` a :lcode:`21-28`).
#. Definujeme vstupní (řádky :lcode:`30-32`) a výstupní (řádky
   :lcode:`34-37`) parametry WPS procesu
#. Implementujeme funkce ``export()`` (:lcode:`39`), která výstupní
   vektorovou mapu exportuje do souboru ve formátu ESRI Shapefile,
   který bude zkomprimován a poslán klientovi.
#. Implementujeme funkci ``execute()`` (:lcode:`61`), která se vykoná
   v okamžiku, kdy od klienta dorazí na server dotaz typu
   ``request=execute``.
#. Vlastní tělo původního skriptu vnoříme do funkce ``run()``
   (:lcode:`66`).
      
.. literalinclude:: ../_static/skripty/obce_psc_wps.py
   :language: python
   :linenos:
   :emphasize-lines: 17, 19, 21-28, 30-32, 34-37, 39, 61, 66

Skript ke stažení `zde <../_static/skripty/obce_psc_wps.py>`__.

Ukázka vypublikovaného procesu
------------------------------

**GetCapabilities**

* http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=getcapabilities

**DescribeProcess**
  
* http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=describeprocess&version=1.0.0&identifier=obce_psc

**Execute**

*
  `http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=execute&identifier=obce_psc&version=1.0.0&datainputs=[psc=41115]
  <http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=execute&identifier=obce_psc&version=1.0.0&datainputs=[psc=41115]>`_
      
