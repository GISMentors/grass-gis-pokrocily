#!/usr/bin/env python

from grass.pygrass.modules import Module

psc = '41115'

Module('v.extract', input='obce', output='obce1',
       where="psc = '{}'".format(psc))
Module('v.select', ainput='obce', binput='obce1',
       output='obce_psc_{}'.format(psc),
       operator='overlap', overwrite=True)
Module('g.remove', type='vector', name='obce1', flags='f')
