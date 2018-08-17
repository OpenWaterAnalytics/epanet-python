

import pytest

from epanet.output import OutputMetadata
from epanet.output import output as oapi

from data import OUTPUT_FILE_EXAMPLE1


def test_outputmetadata_handle():
    
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
        
    handle = oapi.init()
    oapi.open(handle, OUTPUT_FILE_EXAMPLE1)
    
    om = OutputMetadata(handle)
    
    for attr in oapi.NodeAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]
                
    for attr in oapi.LinkAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]

