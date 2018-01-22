#!/usr/bin/env python
from __future__ import print_function

from outbin import EpanetOutBin                 
with EpanetOutBin("example3.bin") as a: 
   name= '217'
   if name in a.nodes:
      node= a.nodes[name]            
      print (node.ID)      
      print (node.demand)       
      print (a.flowunits)                
   else:
      print ("node {0} not found".format(name))