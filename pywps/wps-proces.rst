Vypublikování skriptu jako WPS procesu
======================================

Skript upravíme následovně:

#. Vytvoříme třídu :class:`ObcePsc`, která dědí vlastnosti z třídy
   :class:`Process` (řádky :lcode:`11` a :lcode:`29-39`).
#. Definujeme vstupní (řádky :lcode:`13-19`) a výstupní (řádky
   :lcode:`20-27`) parametry WPS procesu
#. Implementujeme funkci ``_handler()`` (:lcode:`55`), která se vykoná
   v okamžiku, kdy od klienta dorazí na server dotaz typu
   ``request=execute``.
#. Vlastní tělo původního skriptu vnoříme do funkce ``obce_psc()``
   (:lcode:`44`).
      
.. literalinclude:: ../_static/skripty/obce_psc_wps.py
   :language: python
   :linenos:
   :emphasize-lines: 11, 13-19, 20-27, 29-39, 44, 55

Skript ke stažení `zde <../_static/skripty/obce_psc_wps.py>`__.

..
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
      
