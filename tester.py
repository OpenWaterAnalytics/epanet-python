#!/usr/bin/env python
from __future__ import print_function
import epamodule as em
def out(s):
  print (s.decode())

nomeinp= "example3.inp"
nomeout= "example3.txt"
nomebin= "example3.bin"
em.ENepanet(nomeinp, nomeout, nomebin, vfunc=out)