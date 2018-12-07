

#
#  test_toolkit.py
#   
#  Created:    October 19, 2018
#  Author:     Michael E. Tryby
#              US EPA - ORD/NRMRL
#  

import pytest

import epanet.toolkit.toolkit as en

from data import INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST


def test_createdelete():

    _handle = en.proj_create()
    assert(_handle != None)
    
    _handle = en.proj_delete(_handle)
    assert(_handle == None)
    

def test_run():
    _handle = en.proj_create()
    
    en.proj_run(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    
    en.proj_delete(_handle)    
    

def test_openclose():
    _handle = en.proj_create()
    en.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    
    en.proj_close(_handle)
    en.proj_delete(_handle)

 
@pytest.fixture()
def handle(request):    
    _handle = en.proj_create()
    en.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
     
    def close():
        en.proj_close(_handle)
        en.proj_delete(_handle)
     
    request.addfinalizer(close)    
    return _handle    
 

def test_hyd_step(handle): 
     en.hydr_open(handle)
      
     en.hydr_init(handle, en.SaveOption.NOSAVE)
      
     while True:
         time = en.hydr_run(handle)
          
         step = en.hydr_next(handle)
          
         if time == 0.:
             break
 
     en.hydr_close(handle)


def test_qual_step(handle):
    en.hydr_solve(handle)
    
    en.qual_open(handle)
    
    en.qual_init(handle, en.SaveOption.NOSAVE)
    
    while True:
        time = en.qual_run(handle)
        
        step = en.qual_next(handle)
        
        if time == 0.:
            break
        
    en.qual_close(handle)
       

def test_report(handle):
    
    en.hydr_solve(handle)
    en.qual_solve(handle)
    
    en.rprt_set(handle, "NODES ALL")
    en.rprt_writeresults(handle)
    

def test_node(handle):
    index = en.node_getindex(handle, "10")
    id = en.node_getid(handle, index)
    type = en.node_gettype(handle, index)
    coord = en.node_getcoord(handle, index)
    

def test_demand(handle):
    index = en.node_getindex(handle, "10")
    count = en.dmnd_getcount(handle, index)
        

def test_link(handle):
    index = en.link_getindex(handle, "10")
    id = en.link_getid(handle, index)
    type = en.link_gettype(handle, index)
    

def test_pump(handle):
    index = en.link_getindex(handle, "9")
    link_type = en.link_gettype(handle, index)
    pump_type = en.pump_gettype(handle, index)
    

def test_pattern(handle):
    index = en.ptrn_getindex(handle, "1")
    length = en.ptrn_getlength(handle, index)
    

def test_curve(handle):
    index = en.curv_getindex(handle, "1")
    length = en.curv_getlength(handle, index)
    
        
#def test_anlys(handle):
#    
#    en.anlys_getqualinfo()
    

    
# def test_getnodeindex(handle):
#     index = entk.getnodeindex(handle, "13")
#     assert index == 4
#     
# 
# def test_getnodename(handle):
#     id = entk.getnodename(handle, 4)
#     assert id == "13"
#     
# 
# def test_getnodetype(handle):
#     type = entk.getnodetype(handle, 4)
#     assert type == entk.NodeType.JUNCTION.value
#     
#     
# def test_getnodevalue(handle):
#     value = entk.getnodevalue(handle, 4, entk.NodeProperty.ELEVATION)
#     assert value == 695.
#     
# 
# def test_getlinkindex(handle):
#     index = entk.getlinkindex(handle, "31")
#     assert index == 6
#     
#             
# def test_getlinkname(handle):
#     id = entk.getlinkname(handle, 6)
#     assert id == "31"
# 
# 
# def test_getlinktype(handle):
#     type = entk.getlinktype(handle, 6)
#     assert type == entk.LinkType.PIPE.value    
# 
# 
# # def test_getlinknodearray(handle):
# #     nodes = entk.getlinknodearray(handle, 6)
# #     assert len(nodes) == 2
# #     assert node[0] == 10
# #     assert node[1] == 11
#     
# 
# def test_getlinkvalue(handle):
#     value = entk.getlinkvalue(handle, 6, entk.LinkProperty.DIAMETER)
#     assert value == 6.0
#     
#         



    