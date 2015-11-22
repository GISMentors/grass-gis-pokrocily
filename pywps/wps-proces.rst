Vypublikování skriptu jako WPS procesu
======================================

.. literalinclude:: ../_static/skripty/obce_psc_wps.py
   :language: python
   :linenos:

Ukázka vypublikovaného procesu
------------------------------

**GetCapabilities**

* http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=getcapabilities

**DescribeProcess**
  
* http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=describeprocess&version=1.0.0&identifier=obce_psc

**Execute**

* http://geo102.fsv.cvut.cz/services/yfsgwps?service=wps&request=execute&identifier=obce_psc&version=1.0.0&datainputs=[psc=41115]
      
