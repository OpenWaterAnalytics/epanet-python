

import pytest
import numpy as np

from epanet.output import OutputMetadata
from epanet.output import output as oapi

from data import OUTPUT_FILE_EXAMPLE1



@pytest.fixture()
def handle(request):    
    _handle = oapi.init()
    oapi.open(_handle, OUTPUT_FILE_EXAMPLE1)
    
    def close():
        oapi.close(_handle)
    
    request.addfinalizer(close)    
    return _handle    


def test_outputmetadata_handle(handle):
    
    om = OutputMetadata(handle)
        
    ref = {
        oapi.NodeAttribute.DEMAND:      ("Demand",          "gal/min"),
        oapi.NodeAttribute.HEAD:        ("Head",            "ft"),
        oapi.NodeAttribute.PRESSURE:    ("Pressure",        "psi"),
        oapi.NodeAttribute.QUALITY:     ("Quality",         "mg/L"),
         
        oapi.LinkAttribute.FLOW:        ("Flow",            "gal/min"),
        oapi.LinkAttribute.VELOCITY:    ("Velocity",        "ft/sec"),
        oapi.LinkAttribute.HEADLOSS:    ("Unit Headloss",   "ft/1000ft"),
        oapi.LinkAttribute.AVG_QUALITY: ("Quality",         "mg/L"),
        oapi.LinkAttribute.STATUS:      ("Status",          ""),
        oapi.LinkAttribute.SETTING:     ("Setting",         ""),
        oapi.LinkAttribute.RX_RATE:     ("Reaction Rate",   "mg/hr"),
        oapi.LinkAttribute.FRCTN_FCTR:  ("Friction Factor", "unitless")}
    
    for attr in oapi.NodeAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]
                
    for attr in oapi.LinkAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]


def test_getnodeSeries(handle):
    
    ref_array = np.array(
        [119.25731,
        120.45029,
        121.19854,
        122.00622,
        122.37414,
        122.8122,
        122.82034,
        122.90379,
        123.40434,
        123.81807])
    
    array = oapi.getnodeseries(handle, 2, oapi.NodeAttribute.PRESSURE, 0, 10)
    assert len(array) == 10
    
    assert np.allclose(array, ref_array)
        
        
def test_getlinkseries(handle):
    pass

def test_getnodeattribute(handle):
    ref_array = np.array([ 1., 0.44407997, 0.43766347, 0.42827705, 0.41342604, 
        0.42804748, 0.44152543, 0.40502965, 0.38635802, 1., 0.96745253])

    array = oapi.getnodeattribute(handle, 1, oapi.NodeAttribute.QUALITY)
    assert len(array) == 11
    assert np.allclose(array, ref_array)
 

def test_getlinkattribute(handle):
    ref_array = np.array([ 1848.58117676, 1220.42736816, 130.11161804, 
        187.68930054, 119.88839722, 40.46448898, -748.58111572, 478.15377808, 
        191.73458862, 30.11160851, 140.4644928, 59.53551483, 1848.58117676])
    
    array = oapi.getlinkattribute(handle, 1, oapi.LinkAttribute.FLOW)
    assert len(array) == 13             
    assert np.allclose(array, ref_array)


def test_getnoderesult(handle):
    pass

def test_getlinkresult(handle):
    pass