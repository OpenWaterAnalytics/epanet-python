

#
#  test_toolkit.py
#   
#  Created:    October 19, 2018
#  Author:     Michael E. Tryby
#              US EPA - ORD/NRMRL
#  

import pytest

import epanet.toolkit.toolkit as entk

from data import INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST


def test_createdelete():

    _handle = entk.proj_create()
    assert(_handle != None)
    
    _handle = entk.proj_delete(_handle)
    assert(_handle == None)
    

def test_run():
    _handle = entk.proj_create()
    
    entk.proj_run(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    
    entk.proj_delete(_handle)    
    

def test_openclose():
    _handle = entk.proj_create()
    entk.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    
    entk.proj_close(_handle)
    entk.proj_delete(_handle)

 
@pytest.fixture()
def handle(request):    
    _handle = entk.proj_create()
    entk.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
     
    def close():
        entk.proj_close(_handle)
        entk.proj_delete(_handle)
     
    request.addfinalizer(close)    
    return _handle    
 

def test_hyd_step(handle): 
     entk.hyd_open(handle)
      
     entk.hyd_init(handle, entk.SaveOption.NOSAVE)
      
     while True:
         time = entk.hyd_run(handle)
          
         step = entk.hyd_next(handle)
          
         if time == 0.:
             break
 
     entk.hyd_close(handle)


def test_qual_step(handle):
    entk.hyd_solve(handle)
    
    entk.qual_open(handle)
    
    entk.qual_init(handle, entk.SaveOption.NOSAVE)
    
    while True:
        time = entk.qual_run(handle)
        
        step = entk.qual_next(handle)
        
        if time == 0.:
            break
        
    entk.qual_close(handle)
       

    
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



    